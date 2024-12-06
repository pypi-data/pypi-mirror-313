import typing

from ..asset import Token
from ..chain import Chain
from ..chain.constants import SupportedChain
from .scanner import Scanner


SCANNER_URLS: dict[Chain, str] = {
    SupportedChain.ETHEREUM.value: "https://etherscan.io",
    SupportedChain.OPTIMISM.value: "https://optimistic.etherscan.io",
    SupportedChain.BNB.value: "https://bscscan.com",
    SupportedChain.POLYGON.value: "https://polygonscan.com",
    SupportedChain.OPBNB.value: "https://opbnbscan.com",
    SupportedChain.MANTLE.value: "https://explorer.mantle.xyz",
    SupportedChain.BASE.value: "https://basescan.org",
    SupportedChain.MODE.value: "https://modescan.io",
    SupportedChain.ARBITRUM.value: "https://arbiscan.io",
    SupportedChain.CELO.value: "https://explorer.celo.org/mainnet",
    SupportedChain.AVALANCHE_C_CHAIN.value: "https://snowscan.xyz",
    SupportedChain.BLAST.value: "https://blastscan.io",
    SupportedChain.SCROLL.value: "https://scrollscan.com",
    SupportedChain.SOLANA.value: "https://solana.fm",
}


# EIP-3091 Blockchain Scanner
# https://eips.ethereum.org/EIPS/eip-3091
class EIP3091Scanner(Scanner):
    def __init__(self, chain: Chain) -> None:
        self.url = SCANNER_URLS[chain]

    @typing.override
    def address(self, address: str) -> str:
        return f"{self.url}/address/{address}"

    @typing.override
    def transaction(self, transaction_id: str) -> str:
        return f"{self.url}/tx/{transaction_id}"

    @typing.override
    def token(self, token: Token) -> str:
        return f"{self.url}/token/{token.address}"
