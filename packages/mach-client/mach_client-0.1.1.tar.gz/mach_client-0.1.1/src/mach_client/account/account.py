from __future__ import annotations
import abc
from abc import ABC
from typing import Any

from ..chain import Chain


# CAIP-10 Account ID - acts as proxy for an address on a chain
# https://chainagnostic.org/CAIPs/caip-10
class AccountID[ChainType: Chain, Native](ABC):
    __slots__ = ("chain", "native")

    def __init__(self, chain: ChainType, native: Native) -> None:
        self.chain = chain
        self.native = native

    @property
    @abc.abstractmethod
    def address(self) -> str:
        pass

    @property
    def id(self) -> str:
        return f"{self.chain.id}:{self.address}"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, AccountID) and self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.address})"

    def __str__(self):
        return self.address


# An "owned" address, ie. a keypair
class Account[ChainType: Chain, Native](AccountID[ChainType, Native]):
    __slots__ = tuple()

    @property
    @abc.abstractmethod
    def private_key(self) -> str:
        pass

    # This is used when the account will be logged or displayed but we don't want to expose the private key
    @abc.abstractmethod
    def downcast(self) -> AccountID[ChainType, Any]:
        pass
