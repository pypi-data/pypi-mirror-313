from __future__ import annotations
import dataclasses
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


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class SolanaSentTransaction[Chain: SolanaChain](SentTransaction[Chain]):
    client: SolanaClient[Chain]
    signature: Signature

    @property
    @typing.override
    def id(self) -> str:
        return str(self.signature)

    @typing.override
    async def wait_for_receipt(
        self, **kwargs
    ) -> EncodedConfirmedTransactionWithStatusMeta:
        await self.client.native.confirm_transaction(self.signature, **kwargs)
        response = await self.client.native.get_transaction(self.signature)
        assert response.value
        return response.value

    @property
    @typing.override
    def chain(self) -> Chain:
        return self.client.chain


@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class SolanaTransaction[Chain: SolanaChain](Transaction[Chain]):
    client: SolanaClient[Chain]
    transaction: VersionedTransaction

    @classmethod
    async def create(
        cls,
        client: SolanaClient[Chain],
        instructions: Sequence[Instruction],
        signers: Sequence[SolanaAccount[Chain]],
        address_lookup_table_accounts: Sequence[AddressLookupTableAccount] = tuple(),
    ) -> SolanaTransaction[Chain]:
        blockhash = await client.native.get_latest_blockhash()

        message = MessageV0.try_compile(
            payer=signers[0].keypair.pubkey(),
            instructions=instructions,
            address_lookup_table_accounts=address_lookup_table_accounts,
            recent_blockhash=blockhash.value.blockhash,
        )

        native_signers = [signer.keypair for signer in signers]

        transaction = VersionedTransaction(message, native_signers)

        return cls(client=client, transaction=transaction)

    @typing.override
    async def broadcast(
        self, opts: Optional[TxOpts] = None
    ) -> SolanaSentTransaction[Chain]:
        response = await self.client.native.send_transaction(self.transaction, opts)
        return SolanaSentTransaction(client=self.client, signature=response.value)

    @property
    @typing.override
    def chain(self) -> Chain:
        return self.client.chain
