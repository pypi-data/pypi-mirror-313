from __future__ import annotations
import dataclasses
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


@dataclasses.dataclass(frozen=True, kw_only=True, repr=False, slots=True)
class EthereumToken[Chain: EthereumChain](ApprovableToken[Chain]):
    client: EthereumClient[Chain]
    contract: AsyncContract

    @classmethod
    async def from_data(
        cls,
        client: EthereumClient[Chain],
        address: str,
        symbol: Optional[str],
        decimals: Optional[int],
    ) -> EthereumToken[Chain]:
        contract = client.w3.eth.contract(
            address=client.w3.to_checksum_address(address),
            abi=config.erc20_abi,
        )

        if not symbol:
            symbol = typing.cast(str, await contract.functions.symbol().call())

        if not decimals:
            decimals = typing.cast(int, await contract.functions.decimals().call())

        return cls(client=client, contract=contract, symbol=symbol, decimals=decimals)

    @property
    @typing.override
    def chain(self) -> Chain:
        return self.client.chain

    # https://namespaces.chainagnostic.org/eip155/caip19
    @property
    @typing.override
    def asset_namespace(self) -> str:
        return "erc20"

    @property
    @typing.override
    def address(self) -> ChecksumAddress:
        return self.contract.address

    @typing.override
    async def get_balance(self, account_id: EthereumAccountID[Chain]) -> int:
        return await self.contract.functions.balanceOf(account_id.address).call()

    async def create_transfer_transaction(
        self,
        sender: EthereumAccount[Chain],
        recipient: EthereumAccountID[Chain],
        amount: int,
    ) -> EthereumTransaction[Chain]:
        contract_function = self.contract.functions.transfer(recipient.address, amount)
        return await EthereumTransaction.from_contract_function(
            self.client, contract_function, sender
        )

    @typing.override
    async def transfer(
        self,
        sender: EthereumAccount[Chain],
        recipient: EthereumAccountID[Chain],
        amount: int,
    ) -> TxReceipt:
        transaction = await self.create_transfer_transaction(sender, recipient, amount)
        sent_transaction = await transaction.broadcast()
        return await sent_transaction.wait_for_receipt()

    @typing.override
    async def get_allowance(
        self,
        owner: EthereumAccountID[Chain],
        spender: EthereumAccountID[Chain],
    ) -> int:
        return await self.contract.functions.allowance(
            owner.address, spender.address
        ).call()

    async def create_approval_transaction(
        self,
        owner: EthereumAccount[Chain],
        spender: EthereumAccountID[Chain],
        amount: int,
    ) -> EthereumTransaction[Chain]:
        contract_function = self.contract.functions.approve(spender.address, amount)
        return await EthereumTransaction.from_contract_function(
            self.client, contract_function, owner
        )

    @typing.override
    async def approve(
        self,
        owner: EthereumAccount[Chain],
        spender: EthereumAccountID[Chain],
        amount: int,
    ) -> TxReceipt:
        transaction = await self.create_approval_transaction(owner, spender, amount)
        sent_transaction = await transaction.broadcast()
        return await sent_transaction.wait_for_receipt()
