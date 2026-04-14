from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.models import User, WatchlistItem
from app.services.market_service import get_asset, get_market_overview, search_assets

router = APIRouter(prefix="/market", tags=["market"])


@router.get("/overview")
def overview(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    data = get_market_overview()
    watch = db.query(WatchlistItem).filter_by(user_id=current_user.id).all()
    data["watchlist"] = [w.symbol for w in watch]
    return data


@router.get("/search")
def search(q: str):
    return search_assets(q)


@router.get("/asset/{symbol}")
def asset(symbol: str):
    row = get_asset(symbol)
    if not row:
        raise HTTPException(status_code=404, detail="Asset not found")
    row["headlines"] = [
        f"{symbol.upper()} earnings expectations reset higher",
        f"Analysts discuss {symbol.upper()} valuation range",
    ]
    row["summary"] = f"{row['name']} moved {row['change_pct']}% today."
    return row


@router.post("/watchlist/{symbol}")
def add_watchlist(symbol: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not db.query(WatchlistItem).filter_by(user_id=current_user.id, symbol=symbol.upper()).first():
        db.add(WatchlistItem(user_id=current_user.id, symbol=symbol.upper()))
        db.commit()
    return {"ok": True}


@router.delete("/watchlist/{symbol}")
def remove_watchlist(symbol: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    row = db.query(WatchlistItem).filter_by(user_id=current_user.id, symbol=symbol.upper()).first()
    if row:
        db.delete(row)
        db.commit()
    return {"ok": True}
