from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.models import LearningModule, LearningProgress, QuizAttempt, QuizQuestion, User
from app.services.learning_service import complete_module

router = APIRouter(prefix="/learning", tags=["learning"])


class CompletePayload(BaseModel):
    module_id: int
    score: int


@router.get("/modules")
def modules(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(LearningModule).all()


@router.get("/module/{module_id}/quiz")
def module_quiz(module_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    questions = db.query(QuizQuestion).filter_by(module_id=module_id).all()
    return [
        {
            "id": q.id,
            "question": q.question,
            "options": q.options_csv.split(","),
            "explanation": q.explanation,
            "correct_option": q.correct_option,
        }
        for q in questions
    ]


@router.post("/complete")
def complete(payload: CompletePayload, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        return complete_module(db, current_user, payload.module_id, payload.score)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.get("/progress")
def progress(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    rows = db.query(LearningProgress).filter_by(user_id=current_user.id).all()
    attempts = db.query(QuizAttempt).filter_by(user_id=current_user.id).order_by(QuizAttempt.created_at.desc()).limit(20).all()
    return {
        "xp": current_user.xp,
        "level": current_user.level,
        "completed": [r.module_id for r in rows if r.completed],
        "recent_scores": [{"module_id": a.module_id, "score": a.score, "at": a.created_at} for a in attempts],
    }
