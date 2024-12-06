from __future__ import annotations
import asyncio
from decimal import Decimal
import logging
from typing import Any, Optional

from aiohttp import ClientSession
import cachebox
from cachebox import Cache
from pydantic import BaseModel, TypeAdapter

from ... import config
from ...account import AccountID
from ...asset import Token
from ...chain import Chain
from ...chain_client import ChainClient
from ...log import Logger
from .. import utility
from ..types import MachChain
from .types import AssetPricingData, UserAssetData


class AssetInfo(BaseModel):
    id: str
    symbol: str
    name: str
    image: str
    current_price: Decimal
    market_cap: int
    market_cap_rank: int
    fully_diluted_valuation: int
    total_volume: int
    high_24h: Decimal
    low_24h: Decimal
    price_change_24h: Decimal
    price_change_percentage_24h: Decimal
    market_cap_change_24h: int
    market_cap_change_percentage_24h: Decimal
    circulating_supply: Decimal
    total_supply: Decimal
    max_supply: Optional[Decimal]
    ath: Decimal
    ath_change_percentage: Decimal
    ath_date: str
    atl: Decimal
    atl_change_percentage: Decimal
    atl_date: str
    roi: Optional[Decimal]
    last_updated: str


class AssetServer:
    __slots__ = (
        "logger",
        "routes",
        "tokens",
        "session",
    )

    @classmethod
    @cachebox.cached(Cache(0), copy_level=2)
    async def create(
        cls,
        *,
        logger: Logger = logging.getLogger("mach-client"),
    ) -> AssetServer:
        client = cls(logger)
        await client.refresh_assets()
        return client

    def __init__(self, logger: Logger):
        self.logger = logger
        self.routes = config.config.token_server.endpoints.add_backend_url(
            config.config.token_server.url
        )
        self.tokens: dict[Chain, set[Token]] = {}
        self.session = ClientSession()
        self.session.headers.update(
            (
                ("accept", "application/json"),
                ("Content-Type", "application/json"),
            )
        )

    def is_supported(self, token: Token) -> bool:
        return token.chain in self.tokens and token in self.tokens[token.chain]

    @staticmethod
    def _parse_symbol(symbol: str, name: str) -> str:
        """
        A bad heuristic to parse case-sensitive symbols from a lowercase symbol + a name.

        symbol = "usdt", name = "Tether" => "USDT"
        symbol = "usdt", name = "Tether USDt" => "USDt"
        """
        if (start := name.lower().find(symbol)) == -1:
            return symbol.upper()

        return name[start : start + len(symbol)]

    async def _process_chain_data(
        self, chain: Chain, chain_data: dict[str, dict[str, Any]]
    ) -> None:
        chain_client = await ChainClient.create(chain)

        if chain not in self.tokens:
            self.tokens[chain] = set()

        self.tokens[chain].update(
            await asyncio.gather(
                *[
                    Token.register(
                        client=chain_client,
                        address=address,
                        symbol=self._parse_symbol(
                            symbol=token_data["symbol"],
                            name=token_data["name"],
                        ),
                        decimals=None,
                    )
                    for address, token_data in chain_data.items()
                    if address != "native"
                ]
            )
        )

    _assets_validator = TypeAdapter(dict[MachChain, dict[str, dict[str, Any]]])

    async def refresh_assets(self) -> None:
        async with self.session.get(self.routes.assets) as response:
            bytes_result = await utility.to_bytes(response)

        await asyncio.gather(
            *[
                self._process_chain_data(chain.to_chain(), chain_data)
                for chain, chain_data in self._assets_validator.validate_json(
                    bytes_result
                ).items()
            ]
        )

    async def get_asset_info(self, chain: Chain, address: str) -> AssetInfo:
        mach_chain = MachChain.from_chain(chain)
        # TODO: Casing
        url = f"{self.routes.assets}/{mach_chain.name}/{address}"

        async with self.session.get(url) as response:
            bytes_result = await utility.to_bytes(response)

        asset_info = AssetInfo.model_validate_json(bytes_result)

        await Token.register(
            client=await ChainClient.create(chain),
            address=address,
            symbol=self._parse_symbol(asset_info.symbol, asset_info.name),
            decimals=None,
        )

        return asset_info

    async def get_token_info(self, token: Token) -> AssetInfo:
        return await self.get_asset_info(token.chain, token.address)

    async def get_pricing_data(self, token: Token) -> AssetPricingData:
        mach_chain = MachChain.from_chain(token.chain)
        url = f"{self.routes.prices}/{mach_chain.name}/{token.address}"

        async with self.session.get(url) as response:
            bytes_result = await utility.to_bytes(response)

        return AssetPricingData.model_validate_json(bytes_result)

    async def get_price(self, token: Token) -> Decimal:
        pricing_data = await self.get_pricing_data(token)
        return Decimal(pricing_data.price)

    _asset_data_validator = TypeAdapter(dict[MachChain, list[UserAssetData]])

    async def get_raw_token_balances(
        self, account_id: AccountID
    ) -> dict[MachChain, list[UserAssetData]]:
        url = f"{self.routes.users}/{account_id.address}/assets"

        async with self.session.get(url) as response:
            bytes_result = await utility.to_bytes(response)

        return self._asset_data_validator.validate_json(bytes_result)

    async def _process_chain_balance_data(
        self, mach_chain: MachChain, balance_data: list[UserAssetData]
    ) -> dict[Token, int]:
        chain = mach_chain.to_chain()
        chain_client = await ChainClient.create(chain)

        return {
            await Token.register(
                client=chain_client,
                address=asset_data.address,
                symbol=asset_data.symbol,
                decimals=None,
            ): asset_data.balance
            for asset_data in balance_data
        }

    async def get_token_balances(
        self, account_id: AccountID
    ) -> dict[Chain, dict[Token, int]]:
        raw_balances = await self.get_raw_token_balances(account_id)

        result = asyncio.gather(
            *[
                self._process_chain_balance_data(mach_chain, balance_data)
                for mach_chain, balance_data in raw_balances.items()
                if mach_chain.to_chain() is type(account_id.chain)
            ]
        )

        return dict(result)

    async def get_token_balances_in_coins(
        self, account_id: AccountID
    ) -> dict[Chain, dict[Token, Decimal]]:
        raw_balances = await self.get_token_balances(account_id)
        return utility.balances_in_coins(raw_balances)
