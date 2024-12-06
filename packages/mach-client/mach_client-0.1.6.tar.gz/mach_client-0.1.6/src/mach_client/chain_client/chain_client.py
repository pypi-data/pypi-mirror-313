from __future__ import annotations
import abc
from abc import ABC
import dataclasses
from typing import Any

import cachebox
from cachebox import Cache

from ..account import AccountID
from ..chain import Chain, EthereumChain, SolanaChain, TronChain


# Proxy for a chain-specific client
@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class ChainClient[ChainType: Chain](ABC):
    chain: ChainType

    @staticmethod
    @cachebox.cached(Cache(0))
    async def _create(chain: ChainType) -> ChainClient[ChainType]:
        match chain:
            case EthereumChain():
                return await EthereumClient.create(chain)
            case SolanaChain():
                return await SolanaClient.create(chain)
            case TronChain():
                return await TronClient.create(chain)
            case _:
                raise NotImplementedError(f"Unsupported chain: {chain}")

    @classmethod
    @abc.abstractmethod
    async def create(cls, chain: ChainType) -> ChainClient[ChainType]:
        client = await cls._create(chain)

        if not await client.is_connected():
            del cls._create.cache[chain]  # type: ignore
            client = await cls._create(chain)
            assert await client.is_connected(), f"Failed to connect {chain} client"

        return client

    @abc.abstractmethod
    async def close(self) -> None:
        pass

    @abc.abstractmethod
    async def is_connected(self) -> bool:
        pass

    @abc.abstractmethod
    async def get_gas_balance(self, account_id: AccountID[ChainType]) -> int:
        pass

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, ChainClient) and self.chain == other.chain

    def __hash__(self) -> int:
        return hash(self.chain)


# Avoid a circular import
from .ethereum import EthereumClient  # noqa: E402
from .solana import SolanaClient  # noqa: E402
from .tron import TronClient  # noqa: E402
