from __future__ import annotations
import abc
from decimal import Decimal

from ..chain import Chain
from ..chain_client import ChainClient
from ..account import Account, AccountID
from .asset import Asset


# Fungible token
# Caches some frequently accessed metadata
class Token[
    ChainType: Chain,
    Client: ChainClient,
    NativeToken,
    AccountIDType: AccountID,
    AccountType: Account,
    TransactionReceipt,
](Asset[ChainType]):
    __slots__ = ("native", "symbol", "decimals")

    @classmethod
    @abc.abstractmethod
    async def from_data(
        cls,
        client: Client,
        address: str,
        symbol: str,
        decimals: int,
    ) -> Token:
        pass

    def __init__(self, native: NativeToken, symbol: str, decimals: int) -> None:
        self.native = native
        self.symbol = symbol
        self.decimals = decimals

    @property
    def asset_reference(self) -> str:
        return self.address

    @property
    @abc.abstractmethod
    def address(self) -> str:
        pass

    @abc.abstractmethod
    async def get_balance(self, account_id: AccountIDType) -> int:
        pass

    async def get_balance_in_coins(self, account_id: AccountIDType) -> Decimal:
        return Decimal(await self.get_balance(account_id)) / 10**self.decimals

    def to_coins(self, amount: int) -> Decimal:
        return Decimal(amount) / 10**self.decimals

    def format_amount(self, amount: int) -> str:
        return f"{self.to_coins(amount)} {self}"

    @abc.abstractmethod
    async def transfer(
        self,
        sender: AccountType,
        recipient: AccountIDType,
        amount: int,
    ) -> TransactionReceipt:
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


class ApprovableToken[
    ChainType: Chain,
    Client: ChainClient,
    NativeToken,
    AccountIDType: AccountID,
    AccountType: Account,
    TransactionReceipt,
](
    Token[
        ChainType,
        Client,
        NativeToken,
        AccountIDType,
        AccountType,
        TransactionReceipt,
    ]
):
    __slots__ = tuple()

    @abc.abstractmethod
    async def get_allowance(
        self,
        owner: AccountIDType,
        spender: AccountIDType,
    ) -> int:
        pass

    @abc.abstractmethod
    async def approve(
        self,
        owner: AccountType,
        spender: AccountIDType,
        amount: int,
    ) -> TransactionReceipt:
        pass
