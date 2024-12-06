from __future__ import annotations
from collections import defaultdict
from typing import Optional

from ..chain import Chain
from ..chain_client import ChainClient, EthereumClient, SolanaClient, TronClient
from .asset import Asset, GenericAsset
from .ethereum import EthereumToken
from .solana import SolanaToken
from .token import ApprovableToken, Token
from .tron import TronToken


__all__ = [
    "ApprovableToken",
    "Asset",
    "GenericAsset",
    "SolanaToken",
    "Token",
    "EthereumToken",
    "TronToken",
]


lookup_cache: defaultdict[Chain, dict[str, Token]] = defaultdict(dict)


# The client calls this while initializing the configuration, which caches the tokens so that you can look them up by name
async def register_token(
    client: ChainClient, address: str, symbol: Optional[str], decimals: Optional[int]
) -> Token:
    if token := lookup_cache[client.chain].get(address):
        return token

    match client:
        case EthereumClient():
            token = await EthereumToken.from_data(client, address, symbol, decimals)
        case SolanaClient():
            assert symbol
            token = await SolanaToken.from_data(client, address, symbol, decimals)
        case TronClient():
            token = await TronToken.from_data(client, address, symbol, decimals)
        case _ as chain:
            raise NotImplementedError(f"Unimplemented chain: {chain}")

    lookup_cache[token.chain].update(((token.symbol, token), (token.address, token)))

    return token


def lookup_symbol(chain: Chain, symbol: str) -> Token:
    return lookup_cache[chain][symbol]


def try_lookup_symbol(chain: Chain, symbol: str) -> Optional[Token]:
    return lookup_cache[chain].get(symbol)


def lookup_address(chain: Chain, address: str) -> Token:
    return lookup_cache[chain][address]


def parse_from_str(string: str) -> Token:
    chain_str, symbol = string.split(":")
    chain = Chain.from_str(chain_str)
    return lookup_symbol(chain, symbol)
