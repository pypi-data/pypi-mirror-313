from ..chain import Chain, EthereumChain, SolanaChain, TronChain
from .account import Account, AccountID
from .ethereum import EthereumAccount, EthereumAccountID
from .solana import SolanaAccount, SolanaAccountID
from .tron import TronAccount, TronAccountID


__all__ = [
    "Account",
    "AccountID",
    "EthereumAccount",
    "EthereumAccountID",
    "SolanaAccount",
    "SolanaAccountID",
    "TronAccount",
    "TronAccountID",
]


def create_account_id(chain: Chain, address: str) -> AccountID:
    match chain:
        case EthereumChain():
            return EthereumAccountID.from_str(chain, address)
        case SolanaChain():
            return SolanaAccountID.from_str(chain, address)
        case TronChain():
            return TronAccountID.from_str(chain, address)
        case _:
            raise NotImplementedError(f"Unsupported chain: {chain}")


def create_account(chain: Chain, private_key: str) -> Account:
    match chain:
        case EthereumChain():
            return EthereumAccount.from_str(chain, private_key)
        case SolanaChain():
            return SolanaAccount.from_str(chain, private_key)
        case TronChain():
            return TronAccount.from_str(chain, private_key)
        case _:
            raise NotImplementedError(f"Unsupported chain: {chain}")
