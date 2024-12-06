from __future__ import annotations
import typing

from tronpy.async_tron import AsyncTron
from tronpy.providers import AsyncHTTPProvider

from .. import config
from ..account import TronAccountID
from ..chain import TronChain
from .chain_client import ChainClient


class TronClient(ChainClient[TronChain, AsyncTron, TronAccountID]):
    __slots__ = tuple()

    @classmethod
    @typing.override
    async def create(cls, chain: TronChain) -> TronClient:
        provider = AsyncHTTPProvider(config.endpoint_uris[chain])
        client = AsyncTron(provider)
        return cls(chain, client)

    def __init__(self, chain: TronChain, native: AsyncTron) -> None:
        super().__init__(chain, native)

    @typing.override
    async def close(self) -> None:
        if await self.is_connected():
            await self.native.close()

    @typing.override
    async def is_connected(self) -> bool:
        # TODO: is_closed tells us if the connection is closed, but we should also check if the connection is open
        # However, the state enum that tells us if the connection is open is not exposed by the library
        return not self.native.provider.client.is_closed

    @typing.override
    async def get_gas_balance(self, account_id: TronAccountID) -> int:
        return int(
            await self.native.get_account_balance(account_id.address) * 1_000_000
        )
