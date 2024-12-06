from enum import Enum

from .chain import Chain
from .ethereum import EthereumChain
from .solana import SolanaChain
from .tron import TronChain


class SupportedChain(Enum):
    # BITCOIN = "bip122:000000000019d6689c085ae165831e93"

    ETHEREUM = EthereumChain(1)
    OPTIMISM = EthereumChain(10)
    BNB = EthereumChain(56)
    POLYGON = EthereumChain(137)
    OPBNB = EthereumChain(204)
    MANTLE = EthereumChain(5000)
    BASE = EthereumChain(8453)
    MODE = EthereumChain(34443)
    ARBITRUM = EthereumChain(42161)
    CELO = EthereumChain(42220)
    AVALANCHE_C_CHAIN = EthereumChain(43114)
    BLAST = EthereumChain(81457)
    SCROLL = EthereumChain(534352)

    SOLANA = SolanaChain("5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp")

    TRON = TronChain("27Lqcw")


CHAIN_ID_TO_CHAIN = {chain.value.id: chain for chain in SupportedChain}


CHAIN_TO_NAME: dict[Chain, str] = {
    # SupportedChain.BITCOIN.value: "Bitcoin",
    SupportedChain.ETHEREUM.value: "Ethereum",
    SupportedChain.OPTIMISM.value: "Optimism",
    SupportedChain.BNB.value: "BNB",
    SupportedChain.POLYGON.value: "Polygon",
    SupportedChain.OPBNB.value: "opBNB",
    SupportedChain.MANTLE.value: "Mantle",
    SupportedChain.BASE.value: "Base",
    SupportedChain.MODE.value: "Mode",
    SupportedChain.ARBITRUM.value: "Arbitrum",
    SupportedChain.CELO.value: "Celo",
    SupportedChain.AVALANCHE_C_CHAIN.value: "Avalanche",
    SupportedChain.BLAST.value: "Blast",
    SupportedChain.SCROLL.value: "Scroll",
    SupportedChain.SOLANA.value: "Solana",
    SupportedChain.TRON.value: "Tron",
}

NAME_TO_CHAIN = {name: chain for chain, name in CHAIN_TO_NAME.items()}

# This gets set by the MachClient on initialization
# We have to fetch them from the backend because different instances (production, staging, dev) use different LayerZero versions and thus have different IDs
CHAIN_TO_LAYERZERO_ID: dict[Chain, int] = {}

LAYERZERO_ID_TO_CHAIN = {
    layerzero_id: chain for chain, layerzero_id in CHAIN_TO_LAYERZERO_ID.items()
}
