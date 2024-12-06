import typing

from .chain import Chain


class EthereumChain(Chain):
    __slots__ = tuple()

    def __init__(self, chain_id: int) -> None:
        self.native = chain_id

    @property
    @typing.override
    def namespace(self) -> str:
        return "eip155"

    @property
    @typing.override
    def reference(self) -> str:
        return str(self.native)

    @typing.override
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self})"

    @property
    def chain_id(self) -> int:
        return self.native
