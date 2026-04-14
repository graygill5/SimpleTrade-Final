from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.api.deps import get_current_user
from app.models import User
from app.services.ai_service import assistant_reply

router = APIRouter(prefix="/assistant", tags=["assistant"])


class AssistantRequest(BaseModel):
    question: str


@router.post("/ask")
def ask(payload: AssistantRequest, current_user: User = Depends(get_current_user)):
    return {"answer": assistant_reply(current_user, payload.question)}
