from __future__ import annotations
import typing

from solders.keypair import Keypair
from solders.pubkey import Pubkey

from ..chain import SolanaChain
from .account import Account, AccountID


class SolanaAccountID(AccountID[SolanaChain, Pubkey]):
    __slots__ = tuple()

    @classmethod
    def from_str(cls, chain: SolanaChain, address: str) -> SolanaAccountID:
        return cls(chain, Pubkey.from_string(address))

    def __init__(self, chain: SolanaChain, native: Pubkey) -> None:
        super().__init__(chain, native)

    @property
    @typing.override
    def address(self) -> str:
        return str(self.native)


class SolanaAccount(Account[SolanaChain, Keypair]):
    __slots__ = tuple()

    @classmethod
    def from_str(cls, chain: SolanaChain, private_key: str) -> SolanaAccount:
        return cls(chain, Keypair.from_base58_string(private_key))

    def __init__(self, chain: SolanaChain, native: Keypair) -> None:
        super().__init__(chain, native)

    @property
    @typing.override
    def address(self) -> str:
        return str(self.native.pubkey)

    @property
    @typing.override
    def private_key(self) -> str:
        return str(self.native)

    @typing.override
    def downcast(self) -> SolanaAccountID:
        return SolanaAccountID(self.chain, self.native.pubkey())
