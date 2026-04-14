from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models import ChatMessage, User
from app.services.chat_manager import chat_manager

router = APIRouter(prefix="/chat", tags=["chat"])


@router.get("/history/{room}")
def history(room: str, _: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(ChatMessage).filter(ChatMessage.room == room).order_by(ChatMessage.created_at.asc()).limit(100).all()


@router.websocket("/ws/{room}")
async def websocket_chat(websocket: WebSocket, room: str):
    await chat_manager.connect(room, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await chat_manager.broadcast(room, data)
    except WebSocketDisconnect:
        chat_manager.disconnect(room, websocket)
