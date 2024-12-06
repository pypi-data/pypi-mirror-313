from enum import Enum
from typing import Optional

from pydantic import BaseModel

from .book import OrderDirection, OrderExpiration, OrderFunding
from .types import Chain


class LiquiditySource(str, Enum):
    market_maker = "market_maker"
    cctp_direct = "cctp_direct"
    unavailable = "unavailable"


class OrderData(BaseModel):
    contract_address: str
    order_direction: OrderDirection
    order_funding: OrderFunding
    order_expiration: OrderExpiration
    target_address: str
    filler_address: str


class Quote(BaseModel):
    wallet_address: str
    src_chain: Chain
    dst_chain: Chain
    src_amount: int
    dst_amount: int
    bond_amount: int
    bond_fee: int
    src_asset_address: str
    dst_asset_address: str
    bond_asset_address: str
    challenge_offset: int
    challenge_window: int
    invalid_amount: bool
    liquidity_source: LiquiditySource
    created_at: str
    expires_at: str
    order_data: OrderData
    destination_transaction_fee: int
    destination_transaction_fee_usd: float
    destination_transaction_fee_after_subsidy: int
    destination_transaction_fee_after_subsidy_usd: float
    destination_transaction_fee_subsidy_usd: float
    reject_order: bool


class QuoteRequest(BaseModel):
    wallet_address: str
    target_address: Optional[str] = None
    src_chain: Chain
    dst_chain: Chain
    src_asset_address: str
    dst_asset_address: str
    src_amount: int
