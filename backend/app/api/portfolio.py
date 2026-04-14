from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models import Holding, Trade, User
from app.schemas.portfolio import HoldingOut, TradeOut, TradeRequest
from app.services.portfolio_service import execute_trade

router = APIRouter(prefix="/portfolio", tags=["portfolio"])


@router.get("/holdings", response_model=list[HoldingOut])
def holdings(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Holding).filter(Holding.user_id == current_user.id, Holding.quantity > 0).all()


@router.get("/trades", response_model=list[TradeOut])
def trades(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Trade).filter(Trade.user_id == current_user.id).order_by(Trade.created_at.desc()).all()


@router.post("/trade", response_model=TradeOut)
def trade(payload: TradeRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return execute_trade(db, current_user, payload.symbol, payload.side, payload.quantity)
