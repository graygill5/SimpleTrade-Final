from sqlalchemy.orm import Session

from app.models.models import LearningModule, LearningProgress, QuizAttempt, QuizQuestion, RewardLedger, User
from app.services.ai_service import ai_service

DEFAULT_MODULES = [
    ("Stock Market Basics", "How stocks and exchanges work", "Stocks represent ownership in public companies.", 20),
    ("ETFs and Diversification", "Risk spreading fundamentals", "ETFs bundle assets for diversification.", 25),
    ("Risk Management", "Position sizing and drawdown control", "Protect capital before chasing returns.", 30),
    ("Technical Analysis Basics", "Trends and momentum", "Use price action for trade timing context.", 20),
    ("Fundamental Analysis Basics", "Valuation and earnings", "Evaluate business quality and valuation.", 20),
    ("Trading Psychology", "Decision discipline", "Avoid emotional overtrading and FOMO.", 20),
    ("Portfolio Construction", "Allocation strategy", "Match risk profile to diversified allocation.", 25),
]


def seed_learning(db: Session):
    if db.query(LearningModule).count() == 0:
        for title, desc, content, xp in DEFAULT_MODULES:
            db.add(LearningModule(title=title, description=desc, content=content, xp_reward=xp))
        db.commit()

    if db.query(QuizQuestion).count() == 0:
        for module in db.query(LearningModule).all():
            generated = ai_service.generate_quiz_question(module.title)
            db.add(
                QuizQuestion(
                    module_id=module.id,
                    question=generated["question"],
                    options_csv=",".join(generated["options"]),
                    correct_option=generated["correct_option"],
                    explanation=generated["explanation"],
                )
            )
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
