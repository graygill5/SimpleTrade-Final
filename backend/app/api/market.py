from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.models import User, WatchlistItem
from app.services.ai_service import ai_service
from app.services.market_data_service import market_data_service
from app.services.news_service import news_service

router = APIRouter(prefix="/market", tags=["market"])


@router.get("/overview")
def overview(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    data = market_data_service.market_overview()
    data["news"] = news_service.top_market_headlines()
    data["ai_summary"] = ai_service.market_summary(data)
    watch = db.query(WatchlistItem).filter_by(user_id=current_user.id).all()
    data["watchlist"] = [w.symbol for w in watch]
    return data


@router.get("/search")
def search(q: str):
    return market_data_service.search(q)


@router.get("/asset/{symbol}")
def asset(symbol: str):
    quote = market_data_service.quote(symbol)
    if not quote:
        raise HTTPException(status_code=404, detail="Asset not found")
    quote["history"] = market_data_service.history(symbol)
    quote["news"] = news_service.ticker_news(symbol)
    quote["summary"] = ai_service.explain_news(
        f"{symbol.upper()} market context",
        f"Current move: {quote['change_pct']}% with volume {quote['volume']}",
    )
    return quote


@router.post("/watchlist/{symbol}")
def add_watchlist(symbol: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    symbol = symbol.upper()
    if not db.query(WatchlistItem).filter_by(user_id=current_user.id, symbol=symbol).first():
        db.add(WatchlistItem(user_id=current_user.id, symbol=symbol))
        db.commit()
    return {"ok": True}


@router.delete("/watchlist/{symbol}")
def remove_watchlist(symbol: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    row = db.query(WatchlistItem).filter_by(user_id=current_user.id, symbol=symbol.upper()).first()
    if row:
        db.delete(row)
        db.commit()
    return {"ok": True}
