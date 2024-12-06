from __future__ import annotations
import typing

from ..asset import Token
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
    def token(self, token: Token) -> str:
        return f"{self.url}/token20/{token.address}"
