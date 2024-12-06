import typing
from typing import Optional

from tronpy import AsyncContract
from tronpy.async_tron import TAddress
from tronpy.async_contract import AsyncContractMethod

from .. import config
from ..account import TronAccount, TronAccountID
from ..chain import TronChain
from ..chain_client import TronClient
from ..transaction import TronTransaction
from .token import ApprovableToken


class TronToken(
    ApprovableToken[
        TronChain,
        TronClient,
        AsyncContract,
        TronAccountID,
        TronAccount,
        dict,
    ]
):
    __slots__ = ("client",)

    @classmethod
    @typing.override
    async def from_data(
        cls,
        client: TronClient,
        address: str,
        symbol: Optional[str],
        decimals: Optional[int],
    ):
        native = await client.native.get_contract(address)
        assert native.address
        native.abi = config.erc20_abi

        if not symbol:
            symbol = typing.cast(str, await native.functions.symbol())

        if not decimals:
            decimals = typing.cast(int, await native.functions.decimals())

        return cls(client, native, symbol, decimals)

    def __init__(
        self, client: TronClient, native: AsyncContract, symbol: str, decimals: int
    ) -> None:
        super().__init__(native, symbol, decimals)
        self.client = client

    @property
    @typing.override
    def chain(self) -> TronChain:
        return self.client.chain

    @property
    @typing.override
    def asset_namespace(self) -> str:
        return "trc20"

    @property
    @typing.override
    def address(self) -> TAddress:
        return self.native.address  # type: ignore

    @typing.override
    async def get_balance(self, account_id: TronAccountID) -> int:
        return await self.native.functions.balanceOf(account_id.address)

    async def create_transfer_transaction(
        self,
        sender: TronAccount,
        recipient: TronAccountID,
        amount: int,
    ) -> TronTransaction:
        return await TronTransaction.from_contract_method(
            self.chain,
            sender,
            typing.cast(AsyncContractMethod, self.native.functions.transfer),
            recipient.native,
            amount,
        )

    @typing.override
    async def transfer(
        self,
        sender: TronAccount,
        recipient: TronAccountID,
        amount: int,
    ) -> dict:
        transaction = await self.create_transfer_transaction(sender, recipient, amount)
        sent_transaction = await transaction.broadcast()
        return await sent_transaction.wait_for_receipt()

    @typing.override
    async def get_allowance(self, owner: TronAccountID, spender: TronAccountID) -> int:
        return await self.native.functions.allowance(owner.address, spender.address)

    async def create_approval_transaction(
        self,
        owner: TronAccount,
        spender: TronAccountID,
        amount: int,
    ) -> TronTransaction:
        return await TronTransaction.from_contract_method(
            self.chain,
            owner,
            typing.cast(AsyncContractMethod, self.native.functions.approve),
            spender.native,
            amount,
        )

    @typing.override
    async def approve(
        self,
        owner: TronAccount,
        spender: TronAccountID,
        amount: int,
    ) -> dict:
        transaction = await self.create_approval_transaction(owner, spender, amount)
        sent_transaction = await transaction.broadcast()
        return await sent_transaction.wait_for_receipt()
