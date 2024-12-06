import abc
from abc import ABC
import dataclasses
from typing import Any


from ..chain import Chain


# Proxy for a chain-specific sent transaction
@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class SentTransaction[ChainType: Chain](ABC):
    @property
    @abc.abstractmethod
    def id(self) -> str:
        pass

    @abc.abstractmethod
    async def wait_for_receipt(self, **kwargs) -> Any:
        pass

    @property
    @abc.abstractmethod
    def chain(self) -> ChainType:
        pass


# Proxy for a chain-specific transaction
@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class Transaction[
    ChainType: Chain,
](ABC):
    @abc.abstractmethod
    async def broadcast(self) -> SentTransaction[ChainType]:
        pass

    @property
    @abc.abstractmethod
    def chain(self) -> ChainType:
        pass
