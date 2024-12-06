import cachebox
from cachebox import Cache

from ..chain import Chain, EthereumChain, SolanaChain, TronChain
from .chain_client import ChainClient
from .ethereum import EthereumClient
from .solana import SolanaClient
from .tron import TronClient


__all__ = ["ChainClient", "EthereumClient", "SolanaClient", "TronClient", "create"]


@cachebox.cached(Cache(0))
async def _create(chain: Chain) -> ChainClient:
    match chain:
        case EthereumChain():
            return await EthereumClient.create(chain)
        case SolanaChain():
            return await SolanaClient.create(chain)
        case TronChain():
            return await TronClient.create(chain)
        case _:
            raise NotImplementedError(f"Unsupported chain: {chain}")


async def create(chain: Chain) -> ChainClient:
    client = await _create(chain)

    if not await client.is_connected():
        del _create.cache[chain]  # type: ignore
        client = await _create(chain)
        assert await client.is_connected(), f"Failed to connect {chain} client"

    return client
