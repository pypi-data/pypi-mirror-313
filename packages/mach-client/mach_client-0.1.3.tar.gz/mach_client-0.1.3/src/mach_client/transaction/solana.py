from __future__ import annotations
import typing
from typing import Optional, Sequence

from solana.rpc.types import TxOpts
from solders.address_lookup_table_account import AddressLookupTableAccount
from solders.transaction_status import EncodedConfirmedTransactionWithStatusMeta
from solders.instruction import Instruction
from solders.message import MessageV0
from solders.signature import Signature
from solders.transaction import VersionedTransaction

from ..account import SolanaAccount
from ..chain import SolanaChain
from ..chain_client import SolanaClient
from .transaction import SentTransaction, Transaction


class SolanaSentTransaction(
    SentTransaction[SolanaChain, Signature, EncodedConfirmedTransactionWithStatusMeta]
):
    __slots__ = ("client",)

    def __init__(self, client: SolanaClient, native: Signature) -> None:
        super().__init__(native)
        self.client = client

    @property
    @typing.override
    def id(self) -> str:
        return str(self.native)

    @typing.override
    async def wait_for_receipt(
        self, **kwargs
    ) -> EncodedConfirmedTransactionWithStatusMeta:
        await self.client.native.confirm_transaction(self.native, **kwargs)
        response = await self.client.native.get_transaction(self.native)
        assert response.value
        return response.value

    @property
    @typing.override
    def chain(self) -> SolanaChain:
        return self.client.chain


class SolanaTransaction(
    Transaction[SolanaChain, VersionedTransaction, SolanaSentTransaction]
):
    __slots__ = ("client",)

    @classmethod
    async def create(
        cls,
        client: SolanaClient,
        instructions: Sequence[Instruction],
        signers: Sequence[SolanaAccount],
        address_lookup_table_accounts: Sequence[AddressLookupTableAccount] = tuple(),
    ) -> SolanaTransaction:
        blockhash = await client.native.get_latest_blockhash()

        message = MessageV0.try_compile(
            payer=signers[0].native.pubkey(),
            instructions=instructions,
            address_lookup_table_accounts=address_lookup_table_accounts,
            recent_blockhash=blockhash.value.blockhash,
        )

        native_signers = [signer.native for signer in signers]

        transaction = VersionedTransaction(message, native_signers)

        return cls(client, transaction)

    def __init__(self, client: SolanaClient, native: VersionedTransaction) -> None:
        super().__init__(native)
        self.client = client

    @typing.override
    async def broadcast(self, opts: Optional[TxOpts] = None) -> SolanaSentTransaction:
        response = await self.client.native.send_transaction(self.native, opts)
        return SolanaSentTransaction(self.client, response.value)

    @property
    @typing.override
    def chain(self) -> SolanaChain:
        return self.client.chain
