from __future__ import annotations
import abc
from abc import ABC
from typing import Any

from ..account import AccountID
from ..chain import Chain


# Proxy for a chain-specific client
class ChainClient[ChainType: Chain, NativeClient, AccountIDType: AccountID](ABC):
    __slots__ = ("chain", "native")

    @classmethod
    @abc.abstractmethod
    async def create(cls, chain: ChainType) -> ChainClient:
        pass

    def __init__(self, chain: ChainType, native: NativeClient) -> None:
        self.chain = chain
        self.native = native

    @abc.abstractmethod
    async def close(self) -> None:
        pass

    @abc.abstractmethod
    async def is_connected(self) -> bool:
        pass

    @abc.abstractmethod
    async def get_gas_balance(self, account_id: AccountIDType) -> int:
        pass

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, ChainClient) and self.chain == other.chain

    def __hash__(self) -> int:
        return hash(self.chain)
