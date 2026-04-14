from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.models import FriendRequest, Friendship, Notification, User

router = APIRouter(prefix="/social", tags=["social"])


@router.get("/users")
def search_users(q: str = "", db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(User).filter(User.username.ilike(f"%{q}%")).limit(20).all()


@router.post("/friend-request/{recipient_id}")
def send_request(recipient_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if recipient_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot friend yourself")
    row = FriendRequest(sender_id=current_user.id, recipient_id=recipient_id, status="pending")
    db.add(row)
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
