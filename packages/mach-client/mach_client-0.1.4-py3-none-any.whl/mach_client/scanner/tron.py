from __future__ import annotations
import typing

from ..asset import TronToken
from .scanner import Scanner


class TronScanner(Scanner):
    url = "https://tronscan.io/#"

    @typing.override
    def address(self, address: str) -> str:
        return f"{self.url}/address/{address}"

    @typing.override
    def transaction(self, transaction_id: str) -> str:
        return f"{self.url}/transaction/{transaction_id}"

    @typing.override
    def token(self, token: TronToken) -> str:
        return f"{self.url}/token20/{token.address}"
