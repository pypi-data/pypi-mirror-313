import typing
from typing import Optional

from eth_typing import ChecksumAddress
from web3.contract import AsyncContract
from web3.types import TxReceipt

from .. import config
from ..account import EthereumAccount, EthereumAccountID
from ..chain import EthereumChain
from ..chain_client import EthereumClient
from ..transaction import EthereumTransaction
from .token import ApprovableToken


class EthereumToken(
    ApprovableToken[
        EthereumChain,
        EthereumClient,
        AsyncContract,
        EthereumAccountID,
        EthereumAccount,
        TxReceipt,
    ]
):
    __slots__ = ("client",)

    @classmethod
    @typing.override
    async def from_data(
        cls,
        client: EthereumClient,
        address: str,
        symbol: Optional[str],
        decimals: Optional[int],
    ):
        native = client.native.eth.contract(
            address=client.native.to_checksum_address(address),
            abi=config.erc20_abi,
        )

        if not symbol:
            symbol = typing.cast(str, await native.functions.symbol().call())

        if not decimals:
            decimals = typing.cast(int, await native.functions.decimals().call())

        return cls(client, native, symbol, decimals)

    def __init__(
        self, client: EthereumClient, native: AsyncContract, symbol: str, decimals: int
    ) -> None:
        super().__init__(native, symbol, decimals)
        self.client = client

    @property
    @typing.override
    def chain(self) -> EthereumChain:
        return self.client.chain

    # https://namespaces.chainagnostic.org/eip155/caip19
    @property
    @typing.override
    def asset_namespace(self) -> str:
        return "erc20"

    @property
    @typing.override
    def address(self) -> ChecksumAddress:
        return self.native.address

    @typing.override
    async def get_balance(self, account_id: EthereumAccountID) -> int:
        return await self.native.functions.balanceOf(account_id.address).call()

    async def create_transfer_transaction(
        self,
        sender: EthereumAccount,
        recipient: EthereumAccountID,
        amount: int,
    ) -> EthereumTransaction:
        contract_function = self.native.functions.transfer(recipient.address, amount)
        return await EthereumTransaction.from_contract_function(
            self.client, contract_function, sender
        )

    @typing.override
    async def transfer(
        self,
        sender: EthereumAccount,
        recipient: EthereumAccountID,
        amount: int,
    ) -> TxReceipt:
        transaction = await self.create_transfer_transaction(sender, recipient, amount)
        sent_transaction = await transaction.broadcast()
        return await sent_transaction.wait_for_receipt()

    @typing.override
    async def get_allowance(
        self,
        owner: EthereumAccountID,
        spender: EthereumAccountID,
    ) -> int:
        return await self.native.functions.allowance(
            owner.address, spender.address
        ).call()

    async def create_approval_transaction(
        self,
        owner: EthereumAccount,
        spender: EthereumAccountID,
        amount: int,
    ) -> EthereumTransaction:
        contract_function = self.native.functions.approve(spender.address, amount)
        return await EthereumTransaction.from_contract_function(
            self.client, contract_function, owner
        )

    @typing.override
    async def approve(
        self,
        owner: EthereumAccount,
        spender: EthereumAccountID,
        amount: int,
    ) -> TxReceipt:
        transaction = await self.create_approval_transaction(owner, spender, amount)
        sent_transaction = await transaction.broadcast()
        return await sent_transaction.wait_for_receipt()
