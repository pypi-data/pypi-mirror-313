from __future__ import annotations
import dataclasses
import typing

from tronpy import AsyncTron
from tronpy.keys import PrivateKey, PublicKey

from ..chain import TronChain
from .account import Account, AccountID


@dataclasses.dataclass(frozen=True, kw_only=True, repr=False, slots=True)
class TronAccountID[Chain: TronChain](AccountID[Chain]):
    address_: str

    @classmethod
    def from_address(cls, chain: Chain, address: str) -> TronAccountID[Chain]:
        assert AsyncTron.is_base58check_address(address)
        return cls(chain=chain, address_=address)

    @property
    @typing.override
    def address(self) -> str:
        return self.address_


@dataclasses.dataclass(frozen=True, kw_only=True, repr=False, slots=True)
class TronAccount[Chain: TronChain](Account[Chain]):
    private_key_: PrivateKey

    @classmethod
    def from_private_key(cls, chain: Chain, private_key: str) -> TronAccount[Chain]:
        return cls(
            chain=chain,
            private_key_=typing.cast(PrivateKey, PrivateKey.fromhex(private_key)),
        )

    @property
    @typing.override
    def address(self) -> str:
        return typing.cast(
            PublicKey, self.private_key_.public_key
        ).to_base58check_address()

    @property
    @typing.override
    def private_key(self) -> str:
        return self.private_key_.hex()

    @typing.override
    def downcast(self) -> TronAccountID:
        return TronAccountID(chain=self.chain, address_=self.address)
