from typing import Optional

from pydantic import BaseModel

from .types import Chain


class GasResponse(BaseModel):
    gas_estimate: int
    gas_price: int


class OrderRequest(BaseModel):
    chain: Chain
    place_taker_tx: str
    referral_code: Optional[str] = None


class OrderResponse(BaseModel):
    id: str
    taker_address: str
    maker_address: Optional[str] = None
    src_asset_address: str
    dst_asset_address: str
    src_chain: Chain
    dst_chain: Chain
    src_amount: int
    dst_amount: int
    created_at: str
    filled_at: Optional[str] = None
    expires_at: Optional[str] = None
    completed: bool
    place_tx: str
    fill_tx: Optional[str] = None
    eta: int = 0
