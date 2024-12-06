import abc
from abc import ABC
import dataclasses
from typing import Any

from ..chain import Chain


# CAIP-19 Asset Type
# https://chainagnostic.org/CAIPs/caip-19
@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class Asset[ChainType: Chain](ABC):
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
