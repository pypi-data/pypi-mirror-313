from __future__ import annotations
import typing

from tronpy import AsyncTron
from tronpy.keys import PrivateKey, PublicKey

from ..chain import TronChain
from .account import Account, AccountID


class TronAccountID(AccountID[TronChain, str]):
    __slots__ = tuple()

    @classmethod
    def from_str(cls, chain: TronChain, address: str) -> TronAccountID:
        assert AsyncTron.is_base58check_address(address)
        return cls(chain, address)

    def __init__(self, chain: TronChain, native: str) -> None:
        super().__init__(chain, native)

    @property
    @typing.override
    def address(self) -> str:
        return self.native


class TronAccount(Account[TronChain, PrivateKey]):
    __slots__ = tuple()

    @classmethod
    def from_str(cls, chain: TronChain, private_key: str) -> TronAccount:
        return cls(chain, typing.cast(PrivateKey, PrivateKey.fromhex(private_key)))

    def __init__(self, chain: TronChain, native: PrivateKey) -> None:
        super().__init__(chain, native)

    @property
    @typing.override
    def address(self) -> str:
        return typing.cast(PublicKey, self.native.public_key).to_base58check_address()

    @property
    @typing.override
    def private_key(self) -> str:
        return self.native.hex()

    @typing.override
    def downcast(self) -> TronAccountID:
        return TronAccountID(self.chain, self.address)
