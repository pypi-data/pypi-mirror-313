import abc
from abc import ABC


from ..chain import Chain


# Proxy for a chain-specific sent transaction
class SentTransaction[
    ChainType: Chain,
    Native,
    TransactionReceipt,
](ABC):
    __slots__ = ("native",)

    def __init__(self, native: Native) -> None:
        self.native = native

    @property
    @abc.abstractmethod
    def id(self) -> str:
        pass

    @abc.abstractmethod
    async def wait_for_receipt(self, **kwargs) -> TransactionReceipt:
        pass

    @property
    @abc.abstractmethod
    def chain(self) -> ChainType:
        pass


# Proxy for a chain-specific transaction
class Transaction[
    ChainType: Chain,
    Native,
    SentTransactionType: SentTransaction,
](ABC):
    __slots__ = ("native",)

    def __init__(self, native: Native) -> None:
        self.native = native

    @abc.abstractmethod
    async def broadcast(self) -> SentTransactionType:
        pass

    @property
    @abc.abstractmethod
    def chain(self) -> ChainType:
        pass
