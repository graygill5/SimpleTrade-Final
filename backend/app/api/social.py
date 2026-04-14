from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.models import FriendRequest, Friendship, Notification, User, WatchlistItem

router = APIRouter(prefix="/social", tags=["social"])


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


@router.get("/users")
def search_users(q: str = "", db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(User).filter(User.username.ilike(f"%{q}%")).limit(20).all()


@router.post("/friend-request/{recipient_id}")
def send_request(recipient_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if recipient_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot friend yourself")
    db.add(FriendRequest(sender_id=current_user.id, recipient_id=recipient_id, status="pending"))
    db.add(Notification(user_id=recipient_id, kind="friend_request", message=f"{current_user.username} sent a friend request"))
    db.commit()
    return {"ok": True}


@router.post("/friend-request/{request_id}/accept")
def accept_request(request_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    req = db.get(FriendRequest, request_id)
    if not req or req.recipient_id != current_user.id:
        raise HTTPException(status_code=404, detail="Request not found")
    req.status = "accepted"
    db.add(Friendship(user_id=req.sender_id, friend_id=req.recipient_id, is_close_friend=False))
    db.add(Friendship(user_id=req.recipient_id, friend_id=req.sender_id, is_close_friend=False))
    db.add(Notification(user_id=req.sender_id, kind="friend_accept", message=f"{current_user.username} accepted your request"))
    db.commit()
    return {"ok": True}


@router.post("/friend/{friend_id}/close")
def toggle_close(friend_id: int, close: bool = True, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    row = db.query(Friendship).filter_by(user_id=current_user.id, friend_id=friend_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Friendship not found")
    row.is_close_friend = close
    db.commit()
    return {"ok": True, "close": close}


@router.get("/friends")
def friends(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Friendship).filter_by(user_id=current_user.id).all()


@router.get("/notifications")
def list_notifications(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Notification).filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).limit(50).all()


@router.post("/notifications/{notification_id}/read")
def mark_read(notification_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    row = db.get(Notification, notification_id)
    if row and row.user_id == current_user.id:
        row.read = True
        db.commit()
    return {"ok": True}
