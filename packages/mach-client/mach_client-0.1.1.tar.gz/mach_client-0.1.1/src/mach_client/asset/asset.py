import abc
from abc import ABC
import typing
from typing import Any

from ..chain import Chain


# CAIP-19 Asset Type
# https://chainagnostic.org/CAIPs/caip-19
class Asset[ChainType: Chain](ABC):
    __slots__ = tuple()

    @property
    @abc.abstractmethod
    def chain(self) -> ChainType:
        pass

    @property
    @abc.abstractmethod
    def asset_namespace(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def asset_reference(self) -> str:
        pass

    @property
    def id(self) -> str:
        return f"{self.chain.id}/{self.asset_namespace}:{self.asset_reference}"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Asset) and self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.id})"

    def __str__(self) -> str:
        return f"{self.chain}-{self.asset_reference}"


class GenericAsset[ChainType: Chain](Asset[ChainType]):
    __slots__ = ("_chain", "_asset_namespace", "_asset_reference")

    def __init__(
        self, chain: ChainType, asset_namespace: str, asset_reference: str
    ) -> None:
        self._chain = chain
        self._asset_namespace = asset_namespace
        self._asset_reference = asset_reference

    @property
    @typing.override
    def chain(self) -> ChainType:
        return self._chain

    @property
    @typing.override
    def asset_namespace(self) -> str:
        return self._asset_namespace

    @property
    @typing.override
    def asset_reference(self) -> str:
        return self._asset_reference
