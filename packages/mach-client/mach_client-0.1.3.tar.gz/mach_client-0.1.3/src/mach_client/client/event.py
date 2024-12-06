import dataclasses
from datetime import timedelta
from typing import Any

from ..account import AccountID
from ..asset import Token
from ..transaction import SentTransaction, Transaction
from .risk_manager import RiskAnalysis
from .types import OrderResponse, Quote


@dataclasses.dataclass
class InsufficientSourceBalance:
    token: Token
    balance: int
    account_id: AccountID


@dataclasses.dataclass
class QuoteFailed:
    pair: tuple[Token, Token]
    amount: int
    account_id: AccountID
    exception: Exception


@dataclasses.dataclass
class QuoteLiquidityUnavailable:
    pair: tuple[Token, Token]
    amount: int
    account_id: AccountID
    quote: Quote


@dataclasses.dataclass
class RiskManagerRejection:
    pair: tuple[Token, Token]
    amount: int
    quote: Quote
    risk_analysis: RiskAnalysis


@dataclasses.dataclass
class SubmitOrderFailed:
    pair: tuple[Token, Token]
    amount: int
    place_order_transaction: SentTransaction
    exception: Exception


@dataclasses.dataclass
class SourceNotWithdrawn:
    pair: tuple[Token, Token]
    amount: int
    order: OrderResponse
    wait_time: timedelta


@dataclasses.dataclass
class DestinationNotReceived:
    pair: tuple[Token, Token]
    amount: int
    order: OrderResponse
    wait_time: timedelta


@dataclasses.dataclass
class ApprovalFailed:
    token: Token
    amount: int
    owner: AccountID
    spender: AccountID
    exception: Exception


TradeError = (
    InsufficientSourceBalance
    | QuoteFailed
    | QuoteLiquidityUnavailable
    | RiskManagerRejection
    | ApprovalFailed  # Technically this should be a TransactionError, but ApprovableToken.approve() doesn't return events
    | SubmitOrderFailed
    | SourceNotWithdrawn
    | DestinationNotReceived
)


@dataclasses.dataclass
class CreateTransactionFailed:
    data: Any
    exception: Exception


@dataclasses.dataclass
class BroadcastTransactionFailed:
    data: Any
    transaction: Transaction
    exception: Exception


@dataclasses.dataclass
class WaitForTransactionReceiptFailed:
    data: Any
    transaction: SentTransaction
    exception: Exception


TransactionError = (
    CreateTransactionFailed
    | BroadcastTransactionFailed
    | WaitForTransactionReceiptFailed
)


@dataclasses.dataclass
class Trade:
    pair: tuple[Token, Token]
    quote: Quote
    order: OrderResponse


TradeEvent = Trade | TradeError | TransactionError
