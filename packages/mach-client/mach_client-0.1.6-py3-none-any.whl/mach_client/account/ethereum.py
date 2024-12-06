from __future__ import annotations
import dataclasses
import typing

from eth_account import Account as EthAccount
from eth_account.signers.local import LocalAccount
from eth_typing import ChecksumAddress
from web3 import Web3

from ..chain import EthereumChain
from .account import Account, AccountID


@dataclasses.dataclass(frozen=True, kw_only=True, repr=False, slots=True)
class EthereumAccountID[Chain: EthereumChain](AccountID[Chain]):
    address_: ChecksumAddress

    @classmethod
    def from_address(cls, chain: Chain, address: str) -> EthereumAccountID[Chain]:
        assert Web3.is_checksum_address(address)
        return cls(chain=chain, address_=typing.cast(ChecksumAddress, address))

    @property
    @typing.override
    def address(self) -> ChecksumAddress:
        return self.address_


@dataclasses.dataclass(frozen=True, kw_only=True, repr=False, slots=True)
class EthereumAccount[Chain: EthereumChain](Account[Chain]):
    native: LocalAccount

    @classmethod
    def from_private_key(cls, chain: Chain, private_key: str) -> EthereumAccount[Chain]:
        return cls(chain=chain, native=EthAccount.from_key(private_key))

    @property
    @typing.override
    def address(self) -> ChecksumAddress:
        return self.native.address

    @property
    @typing.override
    def private_key(self) -> str:
        return self.native.key.hex()

    @typing.override
    def downcast(self) -> EthereumAccountID:
        return EthereumAccountID(chain=self.chain, address_=self.native.address)
