import dataclasses
import typing

from .chain import Chain


@dataclasses.dataclass(frozen=True, kw_only=True, repr=False, slots=True)
class TronChain(Chain):
    genesis_block_hash: str

    @property
    @typing.override
    def namespace(self) -> str:
        return "tron"

    @property
    @typing.override
    def reference(self) -> str:
        return self.genesis_block_hash
