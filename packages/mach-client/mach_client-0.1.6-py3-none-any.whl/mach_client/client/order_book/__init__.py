from __future__ import annotations
import typing

from tronpy.async_contract import AsyncContractMethod
from eth_typing import ChecksumAddress

from ...account import (
    Account,
    EthereumAccount,
    SolanaAccount,
    TronAccount,
)
from ...chain import Chain
from ...chain_client import (
    ChainClient,
    EthereumClient,
    SolanaClient,
    TronClient,
)
from ...transaction import (
    EthereumTransaction,
    SolanaTransaction,
    Transaction,
    TronTransaction,
)
from ... import config
from ..types import OrderData
from . import solana as solana_orders
from .solana import PlaceOrderArgs, PlaceOrderParams

if typing.TYPE_CHECKING:
    from ... import MachClient


async def create_place_order_transaction[ChainType: Chain](
    client: MachClient,
    chain_client: ChainClient[ChainType],
    order_data: OrderData,
    signer: Account[ChainType],
    order_book_contract_address: str,
) -> Transaction[ChainType]:
    match chain_client:
        case EthereumClient():
            contract = chain_client.w3.eth.contract(
                address=typing.cast(ChecksumAddress, order_book_contract_address),
                abi=config.ethereum_order_book_abi,
            )

            place_order = contract.functions.placeOrder(
                order_data.order_direction.to_eth(),
                order_data.order_funding.to_eth(),
                order_data.order_expiration.to_eth(),
                order_data.target_address,
                order_data.filler_address,
            )

            return await EthereumTransaction.from_contract_function(
                chain_client,
                place_order,
                typing.cast(EthereumAccount, signer),
            )

        case SolanaClient():
            assert False, "TODO"
            place_order_accounts = solana_orders.get_accounts(
                client, chain_client.chain, {}
            )

            place_order_instruction = solana_orders.place_order(
                args=PlaceOrderArgs(
                    params=PlaceOrderParams(
                        source_sell_amount=order_data.order_funding.src_amount_in,
                        min_sell_amount=0,
                        dest_token_mint=[],
                        dest_buy_amount=order_data.order_funding.dst_amount_out,
                        order_id=43,  # What is this?
                        # eid=chain_client.chain.layerzero_id,
                        eid=540,  # What is this?
                    )
                ),
                accounts=place_order_accounts,
                program_id=solana_orders.PROGRAM_ID,
            )

            return await SolanaTransaction.create(
                typing.cast(SolanaClient, chain_client),
                (place_order_instruction,),
                (typing.cast(SolanaAccount, signer),),
            )

        case TronClient():
            contract = await chain_client.native.get_contract(
                order_book_contract_address
            )
            contract.abi = config.tron_order_book_abi

            return await TronTransaction.from_contract_method(
                chain_client.chain,
                typing.cast(TronAccount, signer),
                typing.cast(AsyncContractMethod, contract.functions.placeOrder),
                order_data.order_direction.to_tron(),
                order_data.order_funding.to_tron(),
                order_data.order_expiration.to_tron(),
                order_data.target_address,
                order_data.filler_address,
            )

        case _:
            raise NotImplementedError(chain_client.chain)
