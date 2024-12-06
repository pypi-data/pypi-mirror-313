from __future__ import annotations
import asyncio
import copy
from datetime import datetime, timedelta
from decimal import Decimal
import itertools
import logging
import pprint
from typing import Any, AsyncGenerator, Iterable, Optional

from aiohttp import ClientSession, WSMsgType
import cachebox
from cachebox import Cache
from pydantic import TypeAdapter

from .. import (
    account as account_factory,
    asset as asset_factory,
    chain_client as chain_client_factory,
    config,
)
from ..account import Account, AccountID
from ..asset import ApprovableToken, Token
from ..chain import Chain, EthereumChain, SolanaChain, constants as chain_constants
from ..chain_client import ChainClient
from ..log import LogContextAdapter, Logger
from ..transaction import SentTransaction, Transaction
from .asset_server import AssetServer
from .event import (
    ApprovalFailed,
    BroadcastTransactionFailed,
    CreateTransactionFailed,
    DestinationNotReceived,
    InsufficientSourceBalance,
    TradeEvent,
    QuoteFailed,
    QuoteLiquidityUnavailable,
    RiskManagerRejection,
    SourceNotWithdrawn,
    SubmitOrderFailed,
    Trade,
    TransactionError,
    WaitForTransactionReceiptFailed,
)
from . import order_book, utility
from .risk_manager import RiskManager, SimilarTokenSlippageManager
from .types import (
    AssetInfo,
    GasResponse,
    LiquiditySource,
    MachChain,
    OrderRequest,
    OrderResponse,
    Quote,
    QuoteRequest,
    WalletPoints,
)


# This class is made to be used as a singleton (see below)
class MachClient:
    endpoint_uris = config.endpoint_uris

    __slots__ = (
        "logger",
        "routes",
        "session",
        "raw_deployments",
        "deployments",
        "gas_symbols",
        "chains",
        "tokens",
    )

    @staticmethod
    def _key_maker(_args: tuple, kwargs: dict) -> Any:
        return (
            kwargs.get("backend_url", config.backend_url),
            kwargs.get("logger", logging.getLogger("mach-client")).name,
        )

    @classmethod
    @cachebox.cached(Cache(0), key_maker=_key_maker, copy_level=2)
    async def create(
        cls,
        *,
        backend_url: str = config.backend_url,
        logger: Logger = logging.getLogger("mach-client"),
    ) -> MachClient:
        client = cls(backend_url, logger)
        await client.init()
        return client

    def __init__(self, backend_url: str, logger: Logger):
        self.logger = logger
        self.routes = config.api_routes.add_backend_url(backend_url)
        self.raw_deployments: dict[str, dict[str, Any]] = {}
        self.deployments: dict[Chain, dict[str, Any]] = {}
        self.gas_symbols: dict[Chain, str] = {}
        self.chains: set[Chain] = set()
        self.tokens: dict[Chain, set[Token]] = {}

    async def init(self) -> None:
        self.session = ClientSession()
        self.session.headers.update(
            (
                ("accept", "application/json"),
                ("Content-Type", "application/json"),
            )
        )

        await self.refresh()

    async def close(self) -> None:
        if hasattr(self, "session"):
            await self.session.close()

    async def refresh(self) -> None:
        await self.refresh_config()
        await self.refresh_tokens()

    async def _process_token_data(
        self, chain_client: ChainClient, symbol: str, token_info: dict[str, Any]
    ) -> None:
        chain = chain_client.chain

        # This is the native asset, not a token
        if token_info.get("wrapped"):
            if gas_symbol := self.gas_symbols.get(chain):
                assert symbol == gas_symbol, f"Multiple gas tokens on {chain}"

            self.gas_symbols[chain] = symbol
            return

        self.tokens[chain].add(
            await asset_factory.register_token(
                chain_client,
                token_info["address"],
                symbol,
                token_info["decimals"],
            )
        )

    async def _process_chain_data(
        self, chain_name: str, chain_data: dict[str, Any]
    ) -> Optional[tuple[Chain, dict[str, Any]]]:
        mach_chain = MachChain(chain_name)
        if not (chain := mach_chain.try_to_chain()):
            self.logger.warning(f"Chain {chain_name} is not supported")
            return

        # See note in CHAIN_TO_LAYERZERO_ID declaration
        chain_constants.CHAIN_TO_LAYERZERO_ID[chain] = chain_data["lz_cid"]

        if chain not in self.endpoint_uris:
            self.logger.warning(f"{chain_name} endpoint URI missing from config")
            return

        result = (chain, chain_data)

        chain_client = await chain_client_factory.create(chain)

        self.chains.add(chain)

        if chain not in self.tokens:
            self.tokens[chain] = set()

        await asyncio.gather(
            *(
                self._process_token_data(chain_client, symbol, token_info)
                for symbol, token_info in chain_data["assets"].items()
            )
        )

        # Remove redundant data
        del chain_data["assets"]
        del chain_data["chain_id"]
        del chain_data["lz_cid"]

        return result

    async def refresh_config(self) -> None:
        async with self.session.get(self.routes.get_config) as response:
            self.raw_deployments: dict[str, dict[str, Any]] = (
                await utility.to_json(response)
            )["deployments"]

        result = await asyncio.gather(
            *[
                self._process_chain_data(chain_name, chain_data)
                for chain_name, chain_data in copy.deepcopy(
                    self.raw_deployments
                ).items()
            ]
        )

        self.deployments = dict(filter(lambda data: data, result))  # type: ignore

    async def _refresh_chain(
        self, chain_name: str, chain_assets: Iterable[AssetInfo]
    ) -> None:
        mach_chain = MachChain(chain_name)
        if not (chain := mach_chain.try_to_chain()):
            self.logger.warning(f"Chain {chain_name} is not supported")
            return

        chain_client = await chain_client_factory.create(chain)

        tokens = await asyncio.gather(
            *[
                asset_factory.register_token(
                    client=chain_client,
                    address=asset.address,
                    symbol=asset.symbol,
                    decimals=asset.decimals,
                )
                for asset in chain_assets
                # TODO: This doesn't update the gas symbol list
                if not asset.is_wrapped
            ]
        )

        self.tokens[chain].update(tokens)

    _assets_validator = TypeAdapter(list[AssetInfo])

    async def refresh_tokens(self) -> None:
        async with self.session.get(self.routes.get_all_tokens_from_db) as response:
            bytes_result = await utility.to_bytes(response)

        assets_info = self._assets_validator.validate_json(bytes_result)

        await asyncio.gather(
            *[
                self._refresh_chain(chain_name, chain_assets)
                for chain_name, chain_assets in itertools.groupby(
                    assets_info, key=lambda x: x.chain
                )
            ]
        )

    async def submit_order(
        self,
        place_order_transaction: SentTransaction,
        referral_code: Optional[str] = None,
    ) -> OrderResponse:
        order_request = OrderRequest(
            chain=MachChain.from_chain(place_order_transaction.chain),
            place_taker_tx=place_order_transaction.id,
            referral_code=referral_code,
        )

        async with self.session.post(
            self.routes.orders, json=order_request.model_dump()
        ) as response:
            bytes_result = await utility.to_bytes(response)

        return OrderResponse.model_validate_json(bytes_result)

    _orders_validator = TypeAdapter(list[OrderResponse])

    async def get_orders(self, account_id: AccountID) -> list[OrderResponse]:
        params = {
            "wallet": account_id.address,
        }

        async with self.session.get(self.routes.orders, params=params) as response:
            bytes_result = await utility.to_bytes(response)

        return self._orders_validator.validate_json(bytes_result)

    async def estimate_gas(self, chain: Chain) -> GasResponse:
        params = {"chain": MachChain(chain).name}

        async with self.session.get(self.routes.gas, params=params) as response:
            bytes_result = await utility.to_bytes(response)

        return GasResponse.model_validate_json(bytes_result)

    async def request_quote(
        self,
        src_token: Token,
        dest_token: Token,
        src_amount: int,
        src_account_id: AccountID,
        dest_account_id: AccountID,
    ) -> Quote:
        assert src_token.chain == src_account_id.chain
        assert dest_token.chain == dest_account_id.chain

        quote_request = QuoteRequest(
            wallet_address=src_account_id.address,
            target_address=dest_account_id.address,
            src_chain=MachChain.from_chain(src_token.chain),
            dst_chain=MachChain.from_chain(dest_token.chain),
            src_asset_address=src_token.address,
            dst_asset_address=dest_token.address,
            src_amount=src_amount,
        )

        async with self.session.post(
            self.routes.quotes, json=quote_request.model_dump()
        ) as response:
            bytes_result = await utility.to_bytes(response)

        return Quote.model_validate_json(bytes_result)

    async def get_points(self, account_id: AccountID) -> float:
        assert isinstance(
            account_id.chain, EthereumChain
        ), "Points only supported on Ethereum"

        url = f"{self.routes.points}/{account_id.address}"

        async with self.session.get(url) as response:
            bytes_result = await utility.to_bytes(response)

        return WalletPoints.model_validate_json(bytes_result).points

    _wallet_points_validator = TypeAdapter(list[WalletPoints])

    async def get_all_points(self, limit: int = 10) -> list[WalletPoints]:
        params = {
            "limit": limit,
        }

        async with self.session.get(self.routes.points, params=params) as response:
            bytes_result = await utility.to_bytes(response)

        return self._wallet_points_validator.validate_json(bytes_result)

    async def get_token_balances(
        self, account_id: AccountID
    ) -> dict[Chain, dict[Token, int]]:
        assert isinstance(
            account_id.chain, (EthereumChain, SolanaChain)
        ), "Balances endpoint only supports Ethereum and Solana"

        params = {"wallet_address": account_id.address}

        async with self.session.get(
            self.routes.token_balances, params=params
        ) as response:
            raw_balances: dict[str, dict[str, int]] = (await utility.to_json(response))[
                "balances"
            ]

        balances: dict[Chain, dict[Token, int]] = {}

        for chain_name, chain_balances in raw_balances.items():
            mach_chain = MachChain(chain_name)
            if not (chain := mach_chain.try_to_chain()):
                continue

            gas_symbol = self.gas_symbols.get(chain)

            balances[chain] = {
                asset_factory.lookup_symbol(chain, symbol): balance
                for symbol, balance in chain_balances.items()
                if symbol != gas_symbol and symbol in asset_factory.lookup_cache[chain]
            }

        return balances

    async def get_token_balances_in_coins(
        self, account_id: AccountID
    ) -> dict[Chain, dict[Token, Decimal]]:
        raw_balances = await self.get_token_balances(account_id)
        return utility.balances_in_coins(raw_balances)

    def contract_address(self, chain: Chain, name: str) -> str:
        return self.deployments[chain]["contracts"][name]

    def order_book_contract_address(self, chain: Chain) -> str:
        match chain:
            case EthereumChain():
                return self.contract_address(chain, "order_book_v2")
            case _:
                return self.contract_address(chain, "order_book")

    async def place_logged_transaction(
        self,
        transaction: Transaction,
        logger: Logger,
    ) -> TransactionError | SentTransaction:
        logger.info("Broadcasting transaction")

        try:
            sent_transaction: SentTransaction = await transaction.broadcast()
        except Exception as e:
            logger.error("Failed to broadcast transaction:", exc_info=e)
            return BroadcastTransactionFailed(None, transaction, e)

        logger.info("Waiting for transaction receipt")

        try:
            receipt = await sent_transaction.wait_for_receipt()
        except Exception as e:
            logger.error(f"Could not get receipt for {sent_transaction.id}", exc_info=e)
            return WaitForTransactionReceiptFailed(None, sent_transaction, e)

        logger.info(f"Received receipt: {receipt}")

        return sent_transaction

    async def watch_order_status(
        self, order: OrderResponse
    ) -> AsyncGenerator[OrderResponse]:
        url = f"{self.routes.order_status}/{order.id}"

        async with self.session.ws_connect(url) as websocket:
            async for message in websocket:
                if message.type != WSMsgType.TEXT:
                    continue

                yield OrderResponse.model_validate_json(message.data)

    async def poll_order_status(
        self, order: OrderResponse, poll_time: int
    ) -> AsyncGenerator[Optional[OrderResponse]]:
        url = f"{self.routes.order_status}/{order.id}"

        async with self.session.ws_connect(url) as websocket:
            iter = aiter(websocket)

            while True:
                try:
                    message = await asyncio.wait_for(anext(iter), timeout=poll_time)

                except TimeoutError:
                    yield None
                    continue

                except StopAsyncIteration:
                    break

                if message.type != WSMsgType.TEXT:
                    continue

                yield OrderResponse.model_validate_json(message.data)

    async def place_trade(
        self,
        *,
        src_token: Token,
        dest_token: Token,
        amount: int,
        account: Account,
        recipient: AccountID,
        max_wait_time: timedelta = timedelta(minutes=5),
        risk_manager: Optional[RiskManager] = None,
        logger: Optional[Logger] = None,
    ) -> TradeEvent:
        assert src_token.chain == account.chain
        assert dest_token.chain == recipient.chain
        assert amount > 0
        assert (
            account.address != recipient.address or account.chain != recipient.chain
        ), "Custom recipient not supported yet"

        if not logger:
            logger = self.logger

        logger = LogContextAdapter(logger, f"{src_token} => {dest_token}")

        if not risk_manager:
            risk_manager = SimilarTokenSlippageManager(
                account, config.slippage_tolerance, logger
            )

        initial_src_balance = await src_token.get_balance(account)
        logger.debug(f"{initial_src_balance=}")

        if initial_src_balance < amount:
            logger.warning("Insufficient source balance.")
            return InsufficientSourceBalance(
                src_token, initial_src_balance, account.downcast()
            )

        try:
            quote = await self.request_quote(
                src_token,
                dest_token,
                amount,
                account.downcast(),
                recipient,
            )
        except Exception as e:
            logger.error("Quote request failed:", exc_info=e)
            return QuoteFailed((src_token, dest_token), amount, account.downcast(), e)

        logger.info("Quote:")
        logger.info(pprint.pformat(quote))

        assert quote.src_amount == amount

        if quote.liquidity_source == LiquiditySource.unavailable:
            return QuoteLiquidityUnavailable(
                (src_token, dest_token), amount, account.downcast(), quote
            )

        logger.info(f"Filling order through {quote.liquidity_source}")

        if (risk_analysis := await risk_manager(src_token, dest_token, quote)).reject:
            logger.warning("Order rejected by risk manager with analysis:")
            logger.warning(pprint.pformat(risk_analysis))
            return RiskManagerRejection(
                (src_token, dest_token), amount, quote, risk_analysis
            )

        src_client = await chain_client_factory.create(src_token.chain)

        if isinstance(src_token, ApprovableToken):
            spender = account_factory.create_account_id(
                src_token.chain,
                self.order_book_contract_address(src_token.chain),
            )

            allowance = await src_token.get_allowance(account, spender)

            if allowance < amount:
                logger.info(
                    f"Placing approval transaction for {src_token.format_amount(amount)}"
                )

                try:
                    receipt = await src_token.approve(
                        account,
                        spender,
                        amount,
                    )
                except Exception as e:
                    logger.error("Failed to create approval transaction:", exc_info=e)
                    return ApprovalFailed(
                        src_token,
                        amount,
                        account.downcast(),
                        spender,
                        e,
                    )

                logger.info(f"Approval granted with receipt: {receipt}")

        order_book_contract_address = self.order_book_contract_address(src_client.chain)

        # Needs to be computed before the order is placed
        initial_dest_balance = await dest_token.get_balance(recipient)

        try:
            place_order_transaction = await order_book.create_place_order_transaction(
                self,
                src_client,
                quote.order_data,
                account,
                order_book_contract_address,
            )
        except Exception as e:
            logger.error("Failed to create place order transaction:", exc_info=e)
            return CreateTransactionFailed(
                {
                    "pair": (src_token, dest_token),
                    "order_data": quote.order_data,
                },
                e,
            )

        logger.info("Placing order transaction")

        result = await self.place_logged_transaction(place_order_transaction, logger)

        if isinstance(result, TransactionError):
            result.data = {
                "pair": (src_token, dest_token),
                "amount": amount,
                "order_data": quote.order_data,
            }

            return result

        logger.info("Order placed. Submitting to backend.")

        try:
            order_response = await self.submit_order(result)
        except Exception as e:
            logger.error("Error submitting order to backend:", exc_info=e)
            return SubmitOrderFailed(
                (src_token, dest_token),
                amount,
                result,
                e,
            )

        logger.info("Order submitted to backend with response:")
        logger.info(pprint.pformat(order_response))

        start_time = datetime.now()
        filled_at = None

        async for order in self.poll_order_status(order_response, 15):
            if not order:
                now = datetime.now()
                time_elapsed = now - start_time

                if filled_at and now > filled_at + max_wait_time:
                    return DestinationNotReceived(
                        (src_token, dest_token),
                        amount,
                        order_response,
                        time_elapsed,
                    )

                elif not filled_at and now > start_time + max_wait_time:
                    return SourceNotWithdrawn(
                        (src_token, dest_token),
                        amount,
                        order_response,
                        time_elapsed,
                    )

                continue

            if order.completed:
                logger.info(f"Order complete: {order}")
                break

            elif filled_at:
                logger.warning(
                    f"Unexpected update, order has already been filled: {order}"
                )

            elif order.filled_at:
                filled_at = datetime.fromisoformat(order.filled_at)
                logger.info(f"Order filled: {order}")

            else:
                logger.debug(f"Received order update: {order}")

        filled_amount = initial_src_balance - await src_token.get_balance(account)
        received_amount = await dest_token.get_balance(recipient) - initial_dest_balance

        if filled_amount != amount:
            logger.warning(
                f"Expected to fill {amount} {src_token}, actually filled {filled_amount}"
            )
            assert filled_amount > 0

        if received_amount != quote.dst_amount:
            logger.warning(
                f"Expected to receive {quote.dst_amount} {dest_token}, actually received {received_amount}"
            )
            assert received_amount > 0

        return Trade((src_token, dest_token), quote, order_response)


__all__ = ["AssetServer", "MachClient"]
