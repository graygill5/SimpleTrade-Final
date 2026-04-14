from sqlalchemy import text
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.models import User
from app.services.ai_service import ai_service

router = APIRouter(prefix="/assistant", tags=["assistant"])


class AssistantRequest(BaseModel):
    question: str
    page: str | None = None


@router.post("/ask")
def ask(payload: AssistantRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return ai_service.ask(db, current_user, payload.question, payload.page)


@router.get("/history")
def history(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    conv = db.execute(
        text(
            """
            SELECT m.role, m.content, m.created_at
            FROM assistant_messages m
            JOIN assistant_conversations c ON c.id = m.conversation_id
            WHERE c.user_id = :uid
            ORDER BY m.created_at ASC
            LIMIT 80
            """
        ),
        {"uid": current_user.id},
    )
    return [dict(r._mapping) for r in conv]
