from datetime import datetime

from pydantic import BaseModel


class TradeRequest(BaseModel):
    symbol: str
    side: str
    quantity: float


class HoldingOut(BaseModel):
    symbol: str
    quantity: float
    avg_cost: float
    realized_pnl: float

    class Config:
        from_attributes = True


class TradeOut(BaseModel):
    symbol: str
    side: str
    quantity: float
    price: float
    notional: float
    created_at: datetime

    class Config:
        from_attributes = True
