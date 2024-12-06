from __future__ import annotations
import typing

from eth_account import Account as EthAccount
from eth_account.signers.local import LocalAccount
from eth_typing import ChecksumAddress
from web3 import Web3

from ..chain import EthereumChain
from .account import Account, AccountID


class EthereumAccountID(AccountID[EthereumChain, ChecksumAddress]):
    __slots__ = tuple()

    @classmethod
    def from_str(cls, chain: EthereumChain, address: str) -> EthereumAccountID:
        assert Web3.is_checksum_address(address)
        return cls(chain, typing.cast(ChecksumAddress, address))

    def __init__(self, chain: EthereumChain, native: ChecksumAddress) -> None:
        super().__init__(chain, native)

    @property
    @typing.override
    def address(self) -> str:
        return self.native


class EthereumAccount(Account[EthereumChain, LocalAccount]):
    __slots__ = tuple()

    @classmethod
    def from_str(cls, chain: EthereumChain, private_key: str) -> EthereumAccount:
        return cls(chain, EthAccount.from_key(private_key))

    def __init__(self, chain: EthereumChain, native: LocalAccount) -> None:
        super().__init__(chain, native)

    @property
    @typing.override
    def address(self) -> str:
        return self.native.address

    @property
    @typing.override
    def private_key(self) -> str:
        return self.native.key.hex()

    @typing.override
    def downcast(self) -> EthereumAccountID:
        return EthereumAccountID(self.chain, self.native.address)
