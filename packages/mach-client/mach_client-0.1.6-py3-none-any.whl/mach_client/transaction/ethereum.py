from __future__ import annotations
import dataclasses
import pprint
import typing

from eth_account.datastructures import SignedTransaction
from eth_typing import ChecksumAddress
from hexbytes import HexBytes
from web3 import AsyncWeb3
from web3.contract.async_contract import AsyncContractFunction
from web3.types import TxParams, TxReceipt

from ..account import EthereumAccount
from ..chain import EthereumChain
from ..chain_client import EthereumClient
from .transaction import SentTransaction, Transaction


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class EthereumSentTransaction[Chain: EthereumChain](SentTransaction[Chain]):
    client: EthereumClient[Chain]
    transaction_hash: HexBytes

    @property
    @typing.override
    def id(self) -> str:
        return self.transaction_hash.hex()

    @typing.override
    async def wait_for_receipt(self, **kwargs) -> TxReceipt:
        receipt = await self.client.w3.eth.wait_for_transaction_receipt(
            self.transaction_hash, **kwargs
        )
        assert (
            receipt["status"] == 0x1
        ), f"Transaction failed:\n{pprint.pformat(receipt)}"
        return receipt

    @property
    @typing.override
    def chain(self) -> Chain:
        return self.client.chain


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class EthereumTransaction[Chain: EthereumChain](Transaction[Chain]):
    client: EthereumClient[Chain]
    transaction: SignedTransaction

    @staticmethod
    async def fill_transaction_defaults(
        w3: AsyncWeb3, address: ChecksumAddress
    ) -> TxParams:
        params: TxParams = {
            "from": address,
            "nonce": await w3.eth.get_transaction_count(address, "latest"),
        }
        return params

    @classmethod
    async def from_contract_function(
        cls,
        client: EthereumClient,
        contract_function: AsyncContractFunction,
        signer: EthereumAccount,
    ) -> EthereumTransaction[Chain]:
        params = await cls.fill_transaction_defaults(client.w3, signer.native.address)
        params = await contract_function.build_transaction(params)
        params["gas"] = 3 * params["gas"] // 2  # type: ignore

        signed_transaction = signer.native.sign_transaction(params)  # type: ignore

        return cls(client=client, transaction=signed_transaction)

    @typing.override
    async def broadcast(self) -> EthereumSentTransaction[Chain]:
        transaction_hash = await self.client.w3.eth.send_raw_transaction(
            self.transaction.raw_transaction
        )
        return EthereumSentTransaction(
            client=self.client, transaction_hash=transaction_hash
        )

    @property
    @typing.override
    def chain(self) -> Chain:
        return self.client.chain
