from __future__ import annotations
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


# Original Token Program token, not Token-2022 token
class SolanaToken(
    ApprovableToken[
        SolanaChain,
        SolanaClient,
        Pubkey,
        SolanaAccountID,
        SolanaAccount,
        EncodedConfirmedTransactionWithStatusMeta,
    ]
):
    """
    TODO: I've avoided using AsyncToken as the native representation because it has some ugly behavior for transactions (approvals and transfers):
    - It requires a payer to be set on initialization for some reason.
        - This means for token transactions, you have to do `from copy import copy; token = copy(self.native); token.payer = <acutal payer>; token.transfer(...)`
    - It uses unversioned messages
    - It sends the transaction for you, so you can't use the SolanaTransaction class
    """

    __slots__ = ("client", "token_program_id")

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
    @typing.override
    async def from_data(
        cls,
        client: SolanaClient,
        address: str,
        symbol: Optional[str],
        decimals: Optional[int],
    ) -> SolanaToken:
        # Token mint
        native = Pubkey.from_string(address)

        assert (
            token_account_info_response := await client.native.get_account_info(native)
        ) and (
            token_account_info := token_account_info_response.value
        ), f"Unable to get token account info for {native}"

        assert (token_program_id := token_account_info.owner) in (
            constants.TOKEN_PROGRAM_ID,
            constants.TOKEN_2022_PROGRAM_ID,
        ), f"{token_program_id} is not a valid token program ID"

        if not symbol:
            pda_str, bump = Metadata.find_pda(str(native))
            pda = Pubkey.from_string(pda_str)
            response = await client.native.get_account_info(pda)
            assert (value := response.value)
            metadata = Metadata(value.data)
            symbol = metadata.symbol()

        if not decimals:
            token = cls.make_token(client, native, token_program_id)
            mint_info = await token.get_mint_info()
            decimals = mint_info.decimals

        return cls(client, native, token_program_id, symbol, decimals)

    def __init__(
        self,
        client: SolanaClient,
        native: Pubkey,
        token_program_id: Pubkey,
        symbol: str,
        decimals: int,
    ) -> None:
        super().__init__(native, symbol, decimals)
        self.client = client
        self.token_program_id = token_program_id

    @property
    @typing.override
    def chain(self) -> SolanaChain:
        return self.client.chain

    # https://namespaces.chainagnostic.org/solana/caip19
    @property
    @typing.override
    def asset_namespace(self) -> str:
        return "token"

    @property
    @typing.override
    def address(self) -> str:
        return str(self.native)

    def associated_token_account(self, account_id: Pubkey) -> Pubkey:
        return spl_instructions.get_associated_token_address(
            owner=account_id,
            mint=self.native,
        )

    async def get_raw_balance(self, account_id: SolanaAccountID) -> UiTokenAmount:
        token_account = self.associated_token_account(account_id.native)
        response = await self.client.native.get_token_account_balance(token_account)

        return response.value

    @typing.override
    async def get_balance(self, account_id: SolanaAccountID) -> int:
        raw_balance = await self.get_raw_balance(account_id)
        return int(raw_balance.amount)

    @typing.override
    async def get_balance_in_coins(self, account_id: SolanaAccountID) -> Decimal:
        raw_balance = await self.get_raw_balance(account_id)
        return Decimal(raw_balance.ui_amount_string)

    async def get_token_account_info(self, account_id: SolanaAccountID) -> AccountInfo:
        # TODO: Wanted to avoid using AsyncToken for aforementioned reasons, but method that deserializes the AccountInfo from AsyncClient.get_account_info response is private
        token = self.make_token(self.client, self.native, self.token_program_id)
        token_account = self.associated_token_account(account_id.native)
        token_account_info = await token.get_account_info(token_account)

        return token_account_info

    async def token_account_exists(self, account_id: SolanaAccountID) -> bool:
        token_account_info = await self.get_token_account_info(account_id)
        return token_account_info.is_initialized

    @typing.override
    async def transfer(
        self,
        sender: SolanaAccount,
        recipient: SolanaAccountID,
        amount: int,
    ) -> EncodedConfirmedTransactionWithStatusMeta:
        source = self.associated_token_account(sender.native.pubkey())
        dest = self.associated_token_account(recipient.native)

        transfer_checked_instruction = spl_instructions.transfer_checked(
            TransferCheckedParams(
                program_id=self.token_program_id,
                source=source,
                mint=self.native,
                dest=dest,
                owner=sender.native.pubkey(),
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
                    payer=sender.native.pubkey(),
                    owner=recipient.native,
                    mint=self.native,
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
        owner: SolanaAccountID,
        spender: SolanaAccountID,
    ) -> int:
        account_info = await self.get_token_account_info(owner)

        return (
            account_info.delegated_amount
            if account_info.delegate == spender.native
            else 0
        )

    @typing.override
    async def approve(
        self,
        owner: SolanaAccount,
        spender: SolanaAccountID,
        amount: int,
    ) -> EncodedConfirmedTransactionWithStatusMeta:
        source = self.associated_token_account(owner.native.pubkey())

        instructions = (
            spl_instructions.approve_checked(
                ApproveCheckedParams(
                    program_id=self.token_program_id,
                    source=source,
                    mint=self.native,
                    delegate=spender.native,
                    owner=owner.native.pubkey(),
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
