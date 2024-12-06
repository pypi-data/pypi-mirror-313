import dataclasses
import typing

from .chain import Chain


@dataclasses.dataclass(frozen=True, kw_only=True, repr=False, slots=True)
class EthereumChain(Chain):
    chain_id: int

    @property
    @typing.override
    def namespace(self) -> str:
        return "eip155"

    @property
    @typing.override
    def reference(self) -> str:
        return str(self.chain_id)
