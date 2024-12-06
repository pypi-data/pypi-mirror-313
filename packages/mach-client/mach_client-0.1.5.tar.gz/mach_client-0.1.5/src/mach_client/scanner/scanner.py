from __future__ import annotations
import abc
from abc import ABC

from ..asset import Token


class Scanner(ABC):
    @abc.abstractmethod
    def address(self, address: str) -> str:
        pass

    @abc.abstractmethod
    def transaction(self, transaction_id: str) -> str:
        pass

    @abc.abstractmethod
    def token(self, token: Token) -> str:
        pass
