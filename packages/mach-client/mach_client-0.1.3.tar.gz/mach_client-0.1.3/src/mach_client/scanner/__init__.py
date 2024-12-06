from ..chain import EthereumChain, Chain, TronChain
from .eip3091 import EIP3091Scanner
from .scanner import Scanner
from .tron import TronScanner


def from_chain(chain: Chain) -> Scanner:
    match chain:
        case EthereumChain():
            return EIP3091Scanner(chain)
        case TronChain():
            return TronScanner()
        case _ as chain:
            raise NotImplementedError(f"Unimplemented chain: {chain}")
