from __future__ import annotations
import typing

from solders import system_program

from .place_order import (
    PROGRAM_ID,
    PlaceOrderAccounts,
    PlaceOrderArgs,
    PlaceOrderParams,
    place_order,
)

if typing.TYPE_CHECKING:
    from ... import MachClient
    from ....chain import SolanaChain


__all__ = [
    "PROGRAM_ID",
    "PlaceOrderAccounts",
    "PlaceOrderArgs",
    "PlaceOrderParams",
    "place_order",
]


def get_accounts(
    client: MachClient, chain: SolanaChain, pdas: dict
) -> PlaceOrderAccounts:
    raise NotImplementedError("TODO")
    # wallet = ctx.account

    # accounts = PlaceOrderAccounts(
    #     payer=wallet.public_key,
    #     caller=wallet.public_key,
    #     authority_pda=pdas["authority_pda"],
    #     message_transmitter=pdas["message_transmitter_account"].public_key,
    #     used_nonces=pdas["used_nonces"],
    #     receiver=client.contract_address(chain, "cctp_token_messenger"),
    #     system_program=system_program.ID,
    #     event_authority=pdas["event_authority"].public_key,
    #     program=client.contract_address(chain, "cctp_message_transmitter"),
    # )

    # return accounts
