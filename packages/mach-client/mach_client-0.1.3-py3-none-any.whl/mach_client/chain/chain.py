from __future__ import annotations
import abc
from abc import ABC
import typing
from typing import Any


# CAIP-2 Chain
# https://chainagnostic.org/CAIPs/caip-2
# https://chainagnostic.org/CAIPs/caip-288
class Chain(ABC):
    __slots__ = ("native",)

    @staticmethod
    def from_id(namespace: str, reference: str) -> Chain:
        match namespace:
            case "eip155":
                return EthereumChain(int(reference))
            case "solana":
                return SolanaChain(reference)
            case "tron":
                return TronChain(reference)
            case _:
                return GenericChain(namespace, reference)

    @staticmethod
    def from_str(name: str) -> Chain:
        return constants.NAME_TO_CHAIN[name]

    @staticmethod
    def from_layerzero_id(id: int) -> Chain:
        return constants.LAYERZERO_ID_TO_CHAIN[id]

    @property
    @abc.abstractmethod
    def namespace(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def reference(self) -> str:
        pass

    @property
    def id(self) -> str:
        return f"{self.namespace}:{self.reference}"

    @property
    def layerzero_id(self) -> int:
        return constants.CHAIN_TO_LAYERZERO_ID[self]

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Chain) and self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self})"

    def __str__(self) -> str:
        return constants.CHAIN_TO_NAME[self]


class GenericChain(Chain):
    __slots__ = ("_namespace",)

    def __init__(self, namespace: str, reference: str) -> None:
        self._namespace = namespace
        self.native = reference

    @property
    @typing.override
    def namespace(self) -> str:
        return self._namespace

    @property
    @typing.override
    def reference(self) -> str:
        return self.native


# Break dependency cycle by putting this at the bottom
from . import constants  # noqa: E402
from .ethereum import EthereumChain  # noqa: E402
from .solana import SolanaChain  # noqa: E402
from .tron import TronChain  # noqa: E402
