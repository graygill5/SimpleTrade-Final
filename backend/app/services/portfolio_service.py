from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import Holding, Trade, User
from app.services.market_service import get_price


def execute_trade(db: Session, user: User, symbol: str, side: str, quantity: float) -> Trade:
    symbol = symbol.upper().strip()
    side = side.lower().strip()
    if side not in {"buy", "sell"}:
        raise HTTPException(status_code=400, detail="side must be buy or sell")
    if quantity <= 0:
        raise HTTPException(status_code=400, detail="quantity must be positive")

    price = get_price(symbol)
    notional = price * quantity

    holding = db.query(Holding).filter(Holding.user_id == user.id, Holding.symbol == symbol).first()
    if not holding:
        holding = Holding(user_id=user.id, symbol=symbol, quantity=0, avg_cost=0)
        db.add(holding)

    if side == "buy":
        if user.cash_balance < notional:
            raise HTTPException(status_code=400, detail="Insufficient virtual cash")
        new_quantity = holding.quantity + quantity
        holding.avg_cost = ((holding.avg_cost * holding.quantity) + notional) / new_quantity
        holding.quantity = new_quantity
        user.cash_balance -= notional
    else:
        if holding.quantity < quantity:
            raise HTTPException(status_code=400, detail="Insufficient shares")
        holding.quantity -= quantity
        user.cash_balance += notional

    trade = Trade(
        user_id=user.id,
        symbol=symbol,
        side=side,
        quantity=quantity,
        price=price,
        notional=notional,
    )
    db.add(trade)
    db.commit()
    db.refresh(trade)
    return trade
