from datetime import datetime

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import SessionLocal, get_db
from app.models.models import ChatMembership, ChatMessage, ChatRoom, Presence, User
from app.services.chat_manager import chat_manager

router = APIRouter(prefix="/chat", tags=["chat"])


@router.get("/rooms")
def rooms(_: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(ChatRoom).all()


@router.post("/rooms")
def create_room(name: str, room_type: str = "group", current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    room = ChatRoom(name=name, room_type=room_type)
    db.add(room)
    db.commit()
    db.refresh(room)
    db.add(ChatMembership(room_id=room.id, user_id=current_user.id, role="admin"))
    db.commit()
    return room


@router.get("/rooms/{room_id}/messages")
def room_messages(room_id: int, _: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(ChatMessage).filter_by(room_id=room_id).order_by(ChatMessage.created_at.desc()).limit(100).all()


@router.websocket("/ws/{room_id}/{user_id}")
async def room_ws(websocket: WebSocket, room_id: int, user_id: int):
    db = SessionLocal()
    await chat_manager.connect(room_id, user_id, websocket)
    try:
        presence = db.get(Presence, user_id) or Presence(user_id=user_id)
        presence.is_online = True
        presence.last_active_at = datetime.utcnow()
        db.merge(presence)
        db.commit()
        await chat_manager.room_broadcast(room_id, {"type": "presence", "user_id": user_id, "is_online": True})

        while True:
            payload = await websocket.receive_json()
            kind = payload.get("type", "message")
            if kind == "typing":
                await chat_manager.room_broadcast(room_id, {"type": "typing", "user_id": user_id})
                continue

            body = payload.get("body", "")
            msg = ChatMessage(room_id=room_id, sender_id=user_id, body=body, is_pinned=bool(payload.get("pin", False)))
            db.add(msg)
            db.commit()
            db.refresh(msg)
            await chat_manager.room_broadcast(
                room_id,
                {
                    "type": "message",
                    "id": msg.id,
                    "room_id": room_id,
                    "sender_id": user_id,
                    "body": body,
                    "created_at": msg.created_at.isoformat(),
                },
            )
    except WebSocketDisconnect:
        presence = db.get(Presence, user_id) or Presence(user_id=user_id)
        presence.is_online = False
        presence.last_active_at = datetime.utcnow()
        db.merge(presence)
        db.commit()
        chat_manager.disconnect(room_id, user_id, websocket)
        await chat_manager.room_broadcast(room_id, {"type": "presence", "user_id": user_id, "is_online": False})
    finally:
        db.close()
