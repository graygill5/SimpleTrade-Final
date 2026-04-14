from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models import LearningModule, LearningProgress, RewardLedger, User
from app.services.learning_service import complete_module

router = APIRouter(prefix="/learning", tags=["learning"])


class CompleteModuleRequest(BaseModel):
    module_id: int
    quiz_score: int = 0


@router.get("/modules")
def modules(_: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(LearningModule).all()


@router.get("/progress")
def progress(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    progress_rows = db.query(LearningProgress).filter(LearningProgress.user_id == current_user.id).all()
    rewards = db.query(RewardLedger).filter(RewardLedger.user_id == current_user.id).all()
    return {"progress": progress_rows, "rewards": rewards, "xp": current_user.xp}


@router.post("/complete")
def complete(payload: CompleteModuleRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return complete_module(db, current_user, payload.module_id, payload.quiz_score)
