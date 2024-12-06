from __future__ import annotations
from enum import Enum
from typing import Optional

from pydantic import BaseModel
from pydantic.functional_validators import AfterValidator
from typing_extensions import Annotated
from web3 import Web3


from ...chain import Chain as NativeChain
from ...chain.constants import SupportedChain, NAME_TO_CHAIN


class Chain(str, Enum):
    ethereum = "ethereum"
    bsc = "bsc"
    avalanche = "avalanche"
    polygon = "polygon"
    arbitrum = "arbitrum"
    optimism = "optimism"
    base = "base"
    solana = "solana"
    celo = "celo"
    blast = "blast"
    scroll = "scroll"
    mantle = "mantle"
    opbnb = "opbnb"
    mode = "mode"
    tron = "tron"

    @classmethod
    def from_chain(cls, chain: NativeChain) -> Chain:
        return CLIENT_CHAIN_TO_MACH_CHAIN[chain]

    def to_chain(self) -> NativeChain:
        return MACH_CHAIN_TO_CLIENT_CHAIN[self]

    def try_to_chain(self) -> Optional[NativeChain]:
        return MACH_CHAIN_TO_CLIENT_CHAIN.get(self)


MACH_CHAIN_TO_CLIENT_CHAIN = {
    (Chain(name.lower()) if chain != SupportedChain.BNB.value else Chain.bsc): chain
    for name, chain in NAME_TO_CHAIN.items()
}

CLIENT_CHAIN_TO_MACH_CHAIN = {
    chain: name for name, chain in MACH_CHAIN_TO_CLIENT_CHAIN.items()
}


class AssetInfo(BaseModel):
    chain: Chain
    symbol: str
    address: str
    decimals: int
    usd_est: Optional[int] = None
    is_wrapped: bool = False
    cex_tickers: dict[str, str] = {}
    name: str = ""

    def __hash__(self):
        return hash(
            (
                "Asset",
                self.chain.name,
                self.symbol,
                str(self.address),
                self.is_wrapped,
                self.decimals,
                self.name,
            )
        )


# TODO: This is only for Ethereum, might change if this endpoint starts supporting more chains
Wallet = Annotated[str, AfterValidator(Web3.to_checksum_address)]


class WalletPoints(BaseModel):
    wallet: Wallet
    points: float
