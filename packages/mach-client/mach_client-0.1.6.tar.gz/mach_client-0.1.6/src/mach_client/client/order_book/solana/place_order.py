from __future__ import annotations
from typing import Optional, TypedDict

from borsh_construct import CStruct
from solders import system_program
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey
from spl.token import constants

from .place_order_params import PlaceOrderParams
from .program_id import PROGRAM_ID


class PlaceOrderArgs(TypedDict):
    params: PlaceOrderParams


layout = CStruct("params" / PlaceOrderParams.layout)


class PlaceOrderAccounts(TypedDict):
    authority: Pubkey
    oapp: Pubkey
    admin_panel: Pubkey
    token_mint: Pubkey
    token_account: Pubkey
    match_account: Optional[Pubkey]
    staking_account: Pubkey
    order: Pubkey


def place_order(
    args: PlaceOrderArgs,
    accounts: PlaceOrderAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: Optional[list[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=accounts["oapp"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["admin_panel"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["token_mint"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["token_account"], is_signer=False, is_writable=True
        ),
        (
            AccountMeta(
                pubkey=accounts["match_account"], is_signer=False, is_writable=True
            )
            if accounts["match_account"]
            else AccountMeta(pubkey=program_id, is_signer=False, is_writable=False)
        ),
        AccountMeta(
            pubkey=accounts["staking_account"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=accounts["order"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=system_program.ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=constants.TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"3\xc2\x9b\xafm\x82`j"
    encoded_args = layout.build(
        {
            "params": args["params"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
