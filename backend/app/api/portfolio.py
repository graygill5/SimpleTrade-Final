from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.models import Friendship, Holding, Trade, User
from app.schemas.portfolio import HoldingOut, TradeOut, TradeRequest
from app.services.market_service import get_asset
from app.services.portfolio_service import calculate_portfolio_value, execute_trade

router = APIRouter(prefix="/portfolio", tags=["portfolio"])


@router.get("/summary")
def summary(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    holdings = db.query(Holding).filter(Holding.user_id == current_user.id, Holding.quantity > 0).all()
    rows = []
    for h in holdings:
        asset = get_asset(h.symbol)
        price = asset["price"] if asset else 0
        market_value = round(price * h.quantity, 2)
        unrealized = round((price - h.avg_cost) * h.quantity, 2)
        rows.append(
            {
                "symbol": h.symbol,
                "quantity": h.quantity,
                "avg_cost": h.avg_cost,
                "current_price": price,
                "market_value": market_value,
                "unrealized_pnl": unrealized,
                "realized_pnl": h.realized_pnl,
            }
        )
    return {
        "cash_balance": current_user.cash_balance,
        "buying_power": current_user.cash_balance,
        "total_value": calculate_portfolio_value(db, current_user),
        "holdings": rows,
    }


@router.get("/holdings", response_model=list[HoldingOut])
def holdings(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Holding).filter(Holding.user_id == current_user.id).all()


@router.get("/trades", response_model=list[TradeOut])
def trades(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Trade).filter(Trade.user_id == current_user.id).order_by(Trade.created_at.desc()).limit(200).all()


@router.post("/trade", response_model=TradeOut)
def trade(payload: TradeRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        return execute_trade(db, current_user, payload.symbol, payload.side, payload.quantity)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/friend/{friend_id}")
def friend_view(friend_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    allowed = db.query(Friendship).filter_by(user_id=friend_id, friend_id=current_user.id, is_close_friend=True).first()
    if not allowed:
        raise HTTPException(status_code=403, detail="Not authorized to view portfolio")
    friend = db.get(User, friend_id)
    if not friend:
        raise HTTPException(status_code=404, detail="Friend not found")
    return {"friend_id": friend_id, "summary": summary(friend, db)}
