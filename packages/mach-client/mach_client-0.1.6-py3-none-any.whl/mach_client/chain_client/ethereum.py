from __future__ import annotations
import dataclasses
import typing

from web3 import AsyncWeb3
from web3.middleware import ExtraDataToPOAMiddleware
from web3.providers import (
    AsyncBaseProvider,
    AsyncHTTPProvider,
    AsyncIPCProvider,
    PersistentConnectionProvider,
    WebSocketProvider,
)


from .. import config
from ..account import EthereumAccountID
from ..chain import EthereumChain
from .chain_client import ChainClient


async def make_provider(endpoint_uri: str) -> AsyncBaseProvider:
    if endpoint_uri.startswith("ws://") or endpoint_uri.startswith("wss://"):
        provider = WebSocketProvider(endpoint_uri)
    elif endpoint_uri.startswith("http://") or endpoint_uri.startswith("https://"):
        provider = AsyncHTTPProvider(endpoint_uri)
    elif endpoint_uri.endswith(".ipc"):
        provider = AsyncIPCProvider(endpoint_uri)
    else:
        raise ValueError(f"Invalid endpoint URI: {endpoint_uri}")

    if isinstance(provider, PersistentConnectionProvider):
        await provider.connect()

    return provider


async def make_w3(chain: EthereumChain) -> AsyncWeb3:
    provider = await make_provider(config.config.endpoint_uris[chain])
    w3 = AsyncWeb3(provider)
    w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)
    return w3


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class EthereumClient[Chain: EthereumChain](ChainClient[Chain]):
    w3: AsyncWeb3

    @classmethod
    @typing.override
    async def create(cls, chain: Chain) -> EthereumClient[Chain]:
        w3 = await make_w3(chain)
        return cls(chain=chain, w3=w3)

    @typing.override
    async def close(self) -> None:
        if await self.is_connected():
            await self.w3.provider.disconnect()

    @typing.override
    async def is_connected(self) -> bool:
        return await self.w3.is_connected()

    @typing.override
    async def get_gas_balance(self, account_id: EthereumAccountID[Chain]) -> int:
        return await self.w3.eth.get_balance(account_id.address_)
