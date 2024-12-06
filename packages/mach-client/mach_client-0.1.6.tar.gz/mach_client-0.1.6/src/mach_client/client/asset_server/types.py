from typing import Optional

from pydantic import BaseModel

from ..types import MachChain


class AssetPricingData(BaseModel):
    chain: MachChain
    address: str
    symbol: str
    decimals: int
    price: float
    daily_percent_change: float


class UserAssetData(BaseModel):
    chain: MachChain
    address: str
    balance: int
    symbol: Optional[str]
    price: Optional[float]
    daily_percent_change: Optional[float]
