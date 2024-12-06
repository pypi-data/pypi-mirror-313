from __future__ import annotations
import dataclasses
from decimal import Decimal
import typing
from typing import Optional

from metaplex_python import Metadata
from solders.account_decoder import UiTokenAmount
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.transaction_status import EncodedConfirmedTransactionWithStatusMeta
from spl.token import instructions as spl_instructions
from spl.token.async_client import AsyncToken
from spl.token import constants
from spl.token.core import AccountInfo
from spl.token.instructions import ApproveCheckedParams, TransferCheckedParams

from ..account import SolanaAccount, SolanaAccountID
from ..chain import SolanaChain
from ..chain_client import SolanaClient
from ..transaction import SolanaTransaction
from .token import ApprovableToken


DUMMY_PAYER = Keypair()


@dataclasses.dataclass(frozen=True, kw_only=True, repr=False, slots=True)
class SolanaToken[Chain: SolanaChain](ApprovableToken[Chain]):
    """
    TODO: I've avoided using AsyncToken as the native representation because it has some ugly behavior for transactions (approvals and transfers):
    - It requires a payer to be set on initialization for some reason.
        - This means for token transactions, you have to do `from copy import copy; token = copy(self.native); token.payer = <acutal payer>; token.transfer(...)`
    - It uses unversioned messages
    - It sends the transaction for you, so you can't use the SolanaTransaction class
    """

    client: SolanaClient[Chain]
    mint: Pubkey
    token_program_id: Pubkey

    @staticmethod
    def make_token(
        client: SolanaClient,
        token_id: Pubkey,
        token_program_id: Pubkey,
        payer: Keypair = DUMMY_PAYER,
    ) -> AsyncToken:
        return AsyncToken(
            conn=client.native,
            pubkey=token_id,
            program_id=token_program_id,
            payer=payer,
        )

    @classmethod
    async def from_data(
        cls,
        client: SolanaClient[Chain],
        address: str,
        symbol: Optional[str],
        decimals: Optional[int],
    ) -> SolanaToken[Chain]:
        mint = Pubkey.from_string(address)

        assert (
            token_account_info_response := await client.native.get_account_info(mint)
        ) and (
            token_account_info := token_account_info_response.value
        ), f"Unable to get token account info for {mint}"

        assert (token_program_id := token_account_info.owner) in (
            constants.TOKEN_PROGRAM_ID,
            constants.TOKEN_2022_PROGRAM_ID,
        ), f"{token_program_id} is not a valid token program ID"

        if not symbol:
            pda_str, _bump = Metadata.find_pda(str(mint))
            pda = Pubkey.from_string(pda_str)
            response = await client.native.get_account_info(pda)
            assert (value := response.value)
            metadata = Metadata(value.data)
            symbol = metadata.symbol()

        if not decimals:
            token = cls.make_token(client, mint, token_program_id)
            mint_info = await token.get_mint_info()
            decimals = mint_info.decimals

        return cls(
            client=client,
            mint=mint,
            token_program_id=token_program_id,
            symbol=symbol,
            decimals=decimals,
        )

    @property
    @typing.override
    def chain(self) -> Chain:
        return self.client.chain

    # https://namespaces.chainagnostic.org/solana/caip19
    @property
    @typing.override
    def asset_namespace(self) -> str:
        return "token"

    @property
    @typing.override
    def address(self) -> str:
        return str(self.mint)

    def associated_token_account(self, account_id: Pubkey) -> Pubkey:
        return spl_instructions.get_associated_token_address(
            owner=account_id,
            mint=self.mint,
            token_program_id=self.token_program_id,
        )

    async def get_raw_balance(
        self, account_id: SolanaAccountID[Chain]
    ) -> UiTokenAmount:
        token_account = self.associated_token_account(account_id.pubkey)
        response = await self.client.native.get_token_account_balance(token_account)

        return response.value

    @typing.override
    async def get_balance(self, account_id: SolanaAccountID[Chain]) -> int:
        raw_balance = await self.get_raw_balance(account_id)
        return int(raw_balance.amount)

    @typing.override
    async def get_balance_in_coins(self, account_id: SolanaAccountID[Chain]) -> Decimal:
        raw_balance = await self.get_raw_balance(account_id)
        return Decimal(raw_balance.ui_amount_string)

    async def get_token_account_info(
        self, account_id: SolanaAccountID[Chain]
    ) -> AccountInfo:
        # TODO: Wanted to avoid using AsyncToken for aforementioned reasons, but method that deserializes the AccountInfo from AsyncClient.get_account_info response is private
        token = self.make_token(self.client, self.mint, self.token_program_id)
        token_account = self.associated_token_account(account_id.pubkey)
        token_account_info = await token.get_account_info(token_account)

        return token_account_info

    async def token_account_exists(self, account_id: SolanaAccountID[Chain]) -> bool:
        token_account_info = await self.get_token_account_info(account_id)
        return token_account_info.is_initialized

    @typing.override
    async def transfer(
        self,
        sender: SolanaAccount[Chain],
        recipient: SolanaAccountID[Chain],
        amount: int,
    ) -> EncodedConfirmedTransactionWithStatusMeta:
        source = self.associated_token_account(sender.keypair.pubkey())
        dest = self.associated_token_account(recipient.pubkey)

        transfer_checked_instruction = spl_instructions.transfer_checked(
            TransferCheckedParams(
                program_id=self.token_program_id,
                source=source,
                mint=self.mint,
                dest=dest,
                owner=sender.keypair.pubkey(),
                amount=amount,
                decimals=self.decimals,
            )
        )

        instructions = (
            (transfer_checked_instruction,)
            if await self.token_account_exists(recipient)
            else (
                # TODO: Using this to be safe but we could just use `create_associated_token_account()`
                spl_instructions.create_idempotent_associated_token_account(
                    payer=sender.keypair.pubkey(),
                    owner=recipient.pubkey,
                    mint=self.mint,
                    token_program_id=self.token_program_id,
                ),
                transfer_checked_instruction,
            )
        )

        transaction = await SolanaTransaction.create(
            self.client,
            instructions,
            (sender,),
        )

        sent_transaction = await transaction.broadcast()

        return await sent_transaction.wait_for_receipt()

    @typing.override
    async def get_allowance(
        self,
        owner: SolanaAccountID[Chain],
        spender: SolanaAccountID[Chain],
    ) -> int:
        account_info = await self.get_token_account_info(owner)

        return (
            account_info.delegated_amount
            if account_info.delegate == spender.pubkey
            else 0
        )

    @typing.override
    async def approve(
        self,
        owner: SolanaAccount[Chain],
        spender: SolanaAccountID[Chain],
        amount: int,
    ) -> EncodedConfirmedTransactionWithStatusMeta:
        source = self.associated_token_account(owner.keypair.pubkey())

        instructions = (
            spl_instructions.approve_checked(
                ApproveCheckedParams(
                    program_id=self.token_program_id,
                    source=source,
                    mint=self.mint,
                    delegate=spender.pubkey,
                    owner=owner.keypair.pubkey(),
                    amount=amount,
                    decimals=self.decimals,
                )
            ),
        )

        transaction = await SolanaTransaction.create(
            self.client,
            instructions,
            (owner,),
        )

        sent_transaction = await transaction.broadcast()

        return await sent_transaction.wait_for_receipt()
