from __future__ import annotations
import abc
from abc import ABC
import dataclasses
from typing import Any

from ..chain import Chain, EthereumChain, SolanaChain, TronChain


# CAIP-10 Account ID - acts as proxy for an address on a chain
# https://chainagnostic.org/CAIPs/caip-10
@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class AccountBase[ChainType: Chain](ABC):
    chain: ChainType

    @property
    @abc.abstractmethod
    def address(self) -> str:
        pass

    @property
    def id(self) -> str:
        return f"{self.chain.id}:{self.address}"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, AccountID) and self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.address})"

    def __str__(self):
        return self.address


# Purely the address/public key component
@dataclasses.dataclass(frozen=True, kw_only=True, repr=False, slots=True)
class AccountID[ChainType: Chain](AccountBase[ChainType]):
    @staticmethod
    def from_str(chain: ChainType, address: str) -> AccountID[ChainType]:
        match chain:
            case EthereumChain():
                return EthereumAccountID.from_address(chain, address)
            case SolanaChain():
                return SolanaAccountID.from_pubkey(chain, address)
            case TronChain():
                return TronAccountID.from_address(chain, address)
            case _:
                raise NotImplementedError(f"Unsupported chain: {chain}")

    @staticmethod
    def from_id(namespace: str, reference: str, address: str) -> AccountID:
        chain = Chain.from_id(namespace, reference)
        return AccountID.from_str(chain, address)


# An "owned" address, ie. a keypair or private key
@dataclasses.dataclass(frozen=True, kw_only=True, repr=False, slots=True)
class Account[ChainType: Chain](AccountBase[ChainType]):
    @staticmethod
    def from_str(chain: ChainType, private_key: str) -> Account[ChainType]:
        match chain:
            case EthereumChain():
                return EthereumAccount.from_private_key(chain, private_key)
            case SolanaChain():
                return SolanaAccount.from_private_key(chain, private_key)
            case TronChain():
                return TronAccount.from_private_key(chain, private_key)
            case _:
                raise NotImplementedError(f"Unsupported chain: {chain}")

    @staticmethod
    def from_id(namespace: str, reference: str, private_key: str) -> Account:
        chain = Chain.from_id(namespace, reference)
        return Account.from_str(chain, private_key)

    @property
    @abc.abstractmethod
    def private_key(self) -> str:
        pass

    @abc.abstractmethod
    def downcast(self) -> AccountID[ChainType]:
        pass


# Avoid a circular import
from .ethereum import EthereumAccount, EthereumAccountID  # noqa: E402
from .solana import SolanaAccount, SolanaAccountID  # noqa: E402
from .tron import TronAccount, TronAccountID  # noqa: E402
