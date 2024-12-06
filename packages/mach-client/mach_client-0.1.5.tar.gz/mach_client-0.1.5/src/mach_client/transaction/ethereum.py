from __future__ import annotations
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


__all__ = ["EthereumSentTransaction", "EthereumTransaction"]


class EthereumSentTransaction(SentTransaction[EthereumChain, HexBytes, TxReceipt]):
    __slots__ = ("client",)

    def __init__(self, client: EthereumClient, native: HexBytes) -> None:
        super().__init__(native)
        self.client = client

    @property
    @typing.override
    def id(self) -> str:
        return self.native.hex()

    @typing.override
    async def wait_for_receipt(self, **kwargs) -> TxReceipt:
        receipt = await self.client.native.eth.wait_for_transaction_receipt(
            self.native, **kwargs
        )
        assert (
            receipt["status"] == 0x1
        ), f"Transaction failed:\n{pprint.pformat(receipt)}"
        return receipt

    @property
    @typing.override
    def chain(self) -> EthereumChain:
        return self.client.chain


class EthereumTransaction(
    Transaction[EthereumChain, SignedTransaction, EthereumSentTransaction]
):
    __slots__ = ("client",)

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
    ) -> EthereumTransaction:
        params = await cls.fill_transaction_defaults(
            client.native, signer.native.address
        )
        params = await contract_function.build_transaction(params)
        params["gas"] = 3 * params["gas"] // 2  # type: ignore

        signed_transaction = signer.native.sign_transaction(params)  # type: ignore

        return cls(client, signed_transaction)

    def __init__(self, client: EthereumClient, native: SignedTransaction) -> None:
        super().__init__(native)
        self.client = client

    @typing.override
    async def broadcast(self) -> EthereumSentTransaction:
        transaction_hash = await self.client.native.eth.send_raw_transaction(
            self.native.raw_transaction
        )
        return EthereumSentTransaction(self.client, transaction_hash)

    @property
    @typing.override
    def chain(self) -> EthereumChain:
        return self.client.chain
