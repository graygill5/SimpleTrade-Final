from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.models import Achievement, Holding, PortfolioSnapshot, Trade, User
from app.services.market_service import get_asset


def mark_achievement(db: Session, user_id: int, code: str, title: str):
    exists = db.query(Achievement).filter_by(user_id=user_id, code=code).first()
    if not exists:
        db.add(Achievement(user_id=user_id, code=code, title=title))


def execute_trade(db: Session, user: User, symbol: str, side: str, quantity: float) -> Trade:
    symbol = symbol.upper().strip()
    side = side.lower().strip()
    asset = get_asset(symbol)
    if not asset:
        raise ValueError("Unknown symbol")
    if side not in {"buy", "sell"}:
        raise ValueError("Invalid side")
    if quantity <= 0:
        raise ValueError("Invalid quantity")

    price = asset["price"]
    notional = round(price * quantity, 2)

    holding = db.query(Holding).filter_by(user_id=user.id, symbol=symbol).first()
    if not holding:
        holding = Holding(user_id=user.id, symbol=symbol, quantity=0, avg_cost=0, realized_pnl=0)
        db.add(holding)

    if side == "buy":
        if user.cash_balance < notional:
            raise ValueError("Insufficient virtual cash")
        new_qty = holding.quantity + quantity
        holding.avg_cost = ((holding.avg_cost * holding.quantity) + notional) / new_qty
        holding.quantity = new_qty
        user.cash_balance -= notional
    else:
        if holding.quantity < quantity:
            raise ValueError("Insufficient shares")
        pnl = (price - holding.avg_cost) * quantity
        holding.realized_pnl += pnl
        holding.quantity -= quantity
        user.cash_balance += notional
        if holding.quantity == 0:
            holding.avg_cost = 0

    trade = Trade(user_id=user.id, symbol=symbol, side=side, quantity=quantity, price=price, notional=notional)
    db.add(trade)

    if db.query(Trade).filter_by(user_id=user.id).count() == 0:
        mark_achievement(db, user.id, "first_trade", "First Trade")

    if db.query(Holding).filter(Holding.user_id == user.id, Holding.quantity > 0).count() >= 3:
        mark_achievement(db, user.id, "diversified", "Diversified Portfolio")

    total_value = calculate_portfolio_value(db, user)
    db.add(PortfolioSnapshot(user_id=user.id, total_value=total_value, daily_pnl=0))
    db.commit()
    db.refresh(trade)
    return trade


def calculate_portfolio_value(db: Session, user: User) -> float:
    holdings = db.query(Holding).filter(Holding.user_id == user.id, Holding.quantity > 0).all()
    holdings_val = 0.0
    for h in holdings:
        price = get_asset(h.symbol)["price"] if get_asset(h.symbol) else 0
        holdings_val += h.quantity * price
    return round(user.cash_balance + holdings_val, 2)


def ensure_user_defaults(user: User):
    if user.cash_balance is None:
        user.cash_balance = settings.initial_virtual_cash
