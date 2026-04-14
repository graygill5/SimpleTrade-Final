from sqlalchemy.orm import Session

from app.models import LearningModule, LearningProgress, RewardLedger, User


DEFAULT_MODULES = [
    {
        "title": "What is a Stock?",
        "content": "A stock is a small ownership piece of a company.",
        "xp_reward": 20,
    },
    {
        "title": "Risk vs Reward",
        "content": "Higher potential return usually means higher risk.",
        "xp_reward": 25,
    },
]


def seed_modules(db: Session):
    if db.query(LearningModule).count() == 0:
        for module in DEFAULT_MODULES:
            db.add(LearningModule(**module))
        db.commit()


def complete_module(db: Session, user: User, module_id: int, quiz_score: int) -> LearningProgress:
    progress = (
        db.query(LearningProgress)
        .filter(LearningProgress.user_id == user.id, LearningProgress.module_id == module_id)
        .first()
    )
    if not progress:
        progress = LearningProgress(user_id=user.id, module_id=module_id)
        db.add(progress)

    progress.completed = True
    progress.quiz_score = quiz_score

    module = db.get(LearningModule, module_id)
    xp_gain = module.xp_reward if module else 10
    user.xp += xp_gain
    cash_reward = xp_gain * 10
    user.cash_balance += cash_reward

    db.add(RewardLedger(user_id=user.id, reason=f"Completed module {module_id}", amount=cash_reward))
    db.commit()
    db.refresh(progress)
    return progress
