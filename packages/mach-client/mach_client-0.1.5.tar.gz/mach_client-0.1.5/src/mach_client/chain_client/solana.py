from __future__ import annotations
import typing

from solana.rpc.async_api import AsyncClient

from .. import config
from ..account import SolanaAccountID
from ..chain import SolanaChain
from .chain_client import ChainClient


class SolanaClient(ChainClient[SolanaChain, AsyncClient, SolanaAccountID]):
    __slots__ = tuple()

    @classmethod
    @typing.override
    async def create(cls, chain: SolanaChain) -> SolanaClient:
        client = AsyncClient(config.endpoint_uris[chain])
        return cls(chain, client)

    def __init__(self, chain: SolanaChain, native: AsyncClient) -> None:
        super().__init__(chain, native)

    @typing.override
    async def close(self) -> None:
        if await self.is_connected():
            await self.native.close()

    @typing.override
    async def is_connected(self) -> bool:
        return await self.native.is_connected()

    @typing.override
    async def get_gas_balance(self, account_id: SolanaAccountID) -> int:
        response = await self.native.get_balance(account_id.native)
        return response.value
