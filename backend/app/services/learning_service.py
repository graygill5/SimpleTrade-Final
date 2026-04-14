from sqlalchemy.orm import Session

from app.models.models import LearningModule, LearningProgress, QuizAttempt, QuizQuestion, RewardLedger, User

DEFAULT_MODULES = [
    ("Stock Market Basics", "How stocks and exchanges work", "Stocks represent ownership in a company.", 20),
    ("ETFs and Diversification", "Risk spreading fundamentals", "ETFs bundle many securities together.", 25),
    ("Risk Management", "Position sizing and stops", "Protect downside before chasing upside.", 30),
]


DEFAULT_QUESTIONS = [
    (1, "What does a stock represent?", "Debt,Ownership in a company,Commodity,Currency", "Ownership in a company", "Stocks are equity ownership."),
    (2, "Why use ETFs?", "Lower diversification,Easy diversification,Higher fees only,No risk", "Easy diversification", "ETFs can reduce single-stock risk."),
]


def seed_learning(db: Session):
    if db.query(LearningModule).count() == 0:
        for title, desc, content, xp in DEFAULT_MODULES:
            db.add(LearningModule(title=title, description=desc, content=content, xp_reward=xp))
        db.commit()

    if db.query(QuizQuestion).count() == 0:
        for m_id, q, opts, correct, exp in DEFAULT_QUESTIONS:
            db.add(QuizQuestion(module_id=m_id, question=q, options_csv=opts, correct_option=correct, explanation=exp))
        db.commit()


def complete_module(db: Session, user: User, module_id: int, score: int):
    module = db.get(LearningModule, module_id)
    if not module:
        raise ValueError("Module not found")

    progress = db.query(LearningProgress).filter_by(user_id=user.id, module_id=module_id).first()
    if not progress:
        progress = LearningProgress(user_id=user.id, module_id=module_id, completed=True, last_score=score)
        db.add(progress)
    else:
        progress.completed = True
        progress.last_score = score

    db.add(QuizAttempt(user_id=user.id, module_id=module_id, score=score))
    xp_gain = module.xp_reward
    user.xp += xp_gain
    user.level = max(1, user.xp // 100 + 1)
    reward_cash = xp_gain * 10
    user.cash_balance += reward_cash
    db.add(RewardLedger(user_id=user.id, reason=f"Lesson {module.title}", amount=reward_cash))
    db.commit()
    return {"xp_gain": xp_gain, "reward_cash": reward_cash, "new_level": user.level}
