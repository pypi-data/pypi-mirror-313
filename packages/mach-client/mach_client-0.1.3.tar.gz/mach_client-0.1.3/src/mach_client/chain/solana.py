import typing

from .chain import Chain


class SolanaChain(Chain):
    __slots__ = tuple()

    def __init__(self, genesis_block_hash: str) -> None:
        self.native = genesis_block_hash

    @property
    @typing.override
    def namespace(self) -> str:
        return "solana"

    @property
    @typing.override
    def reference(self) -> str:
        return self.native

    @typing.override
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self})"

    @property
    def genesis_block_hash(self) -> str:
        return self.native
