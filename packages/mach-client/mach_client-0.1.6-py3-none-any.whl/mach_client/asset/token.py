from __future__ import annotations
import abc
import dataclasses
from decimal import Decimal
from collections import defaultdict
import typing
from typing import Any, ClassVar, Optional

from ..chain import Chain
from ..chain_client import ChainClient, EthereumClient, SolanaClient, TronClient
from ..account import Account, AccountID
from .asset import Asset


# Fungible token
# Caches some frequently accessed metadata
@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class Token[ChainType: Chain](Asset[ChainType]):
    lookup_cache: ClassVar[defaultdict[Chain, dict[str, Token]]] = defaultdict(dict)

    symbol: str
    decimals: int

    # The client calls this while initializing the configuration, which caches the tokens so that you can look them up by name
    @staticmethod
    async def register(
        client: ChainClient[ChainType],
        address: str,
        symbol: Optional[str],
        decimals: Optional[int],
    ) -> Token[ChainType]:
        if token := Token.lookup_cache[client.chain].get(address):
            return token

        match client:
            case EthereumClient():
                token = await ethereum.EthereumToken.from_data(
                    client, address, symbol, decimals
                )
            case SolanaClient():
                assert symbol
                token = await solana.SolanaToken.from_data(
                    client, address, symbol, decimals
                )
            case TronClient():
                token = await tron.TronToken.from_data(
                    client, address, symbol, decimals
                )
            case _ as chain:
                raise NotImplementedError(f"Unimplemented chain: {chain}")

        Token.lookup_cache[token.chain].update(
            ((token.symbol, token), (token.address, token))
        )

        return token

    @staticmethod
    def lookup_symbol(chain: ChainType, symbol: str) -> Token[ChainType]:
        return Token.lookup_cache[chain][symbol]

    @staticmethod
    def try_lookup_symbol(chain: ChainType, symbol: str) -> Optional[Token[ChainType]]:
        return Token.lookup_cache[chain].get(symbol)

    @staticmethod
    def lookup_address(chain: ChainType, address: str) -> Token[ChainType]:
        return Token.lookup_cache[chain][address]

    @property
    @typing.override
    def asset_reference(self) -> str:
        return self.address

    @property
    @abc.abstractmethod
    def address(self) -> str:
        pass

    @abc.abstractmethod
    async def get_balance(self, account_id: AccountID[ChainType]) -> int:
        pass

    async def get_balance_in_coins(self, account_id: AccountID[ChainType]) -> Decimal:
        return Decimal(await self.get_balance(account_id)) / 10**self.decimals

    def to_coins(self, amount: int) -> Decimal:
        return Decimal(amount) / 10**self.decimals

    def format_amount(self, amount: int) -> str:
        return f"{self.to_coins(amount)} {self}"

    @abc.abstractmethod
    async def transfer(
        self,
        sender: Account[ChainType],
        recipient: AccountID[ChainType],
        amount: int,
    ) -> Any:
        pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self})"

    def __str__(self) -> str:
        return f"{self.chain}-{self.symbol}"

    def is_stablecoin(self) -> bool:
        return self.symbol in ("FRAX", "DAI", "MIM") or any(
            map(
                lambda symbol: symbol in self.symbol,
                ("USD", "EUR", "JPY", "GPB", "CHF"),
            )
        )

    def is_chf_stablecoin(self) -> bool:
        return "CHF" in self.symbol

    def is_eur_stablecoin(self) -> bool:
        return "EUR" in self.symbol

    def is_gbp_stablecoin(self) -> bool:
        return "GBP" in self.symbol

    def is_jpy_stablecoin(self) -> bool:
        return "JPY" in self.symbol

    def is_usd_stablecoin(self) -> bool:
        return "USD" in self.symbol or self.symbol in ("FRAX", "DAI", "MIM")

    def is_btc(self) -> bool:
        return "BTC" in self.symbol

    def is_eth(self) -> bool:
        return "ETH" in self.symbol


@dataclasses.dataclass(frozen=True, kw_only=True, repr=False, slots=True)
class ApprovableToken[ChainType: Chain](Token[ChainType]):
    @abc.abstractmethod
    async def get_allowance(
        self,
        owner: AccountID[ChainType],
        spender: AccountID[ChainType],
    ) -> int:
        pass

    @abc.abstractmethod
    async def approve(
        self,
        owner: Account[ChainType],
        spender: AccountID[ChainType],
        amount: int,
    ) -> Any:
        pass


# Avoid a circular import
from . import ethereum, solana, tron  # noqa: E402
