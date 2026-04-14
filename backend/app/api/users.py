from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.models import Notification, User, WatchlistItem

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me")
def me(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    watch_count = db.query(WatchlistItem).filter_by(user_id=current_user.id).count()
    unread = db.query(Notification).filter_by(user_id=current_user.id, read=False).count()
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "cash_balance": current_user.cash_balance,
        "xp": current_user.xp,
        "level": current_user.level,
        "watchlist_count": watch_count,
        "unread_notifications": unread,
    }
