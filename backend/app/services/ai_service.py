from app.models import User


def assistant_reply(user: User, question: str) -> str:
    q = question.lower()
    if "portfolio" in q:
        return (
            f"Your paper portfolio has ${user.cash_balance:,.2f} cash available. "
            "Try diversifying across sectors to reduce risk."
        )
    if "xp" in q or "learning" in q:
        return f"You currently have {user.xp} XP. Finish another lesson to earn more rewards."
    if "market" in q:
        return "Markets are moving with mixed momentum today. Focus on trend and risk control."
    return "I can help explain portfolio moves, market updates, and learning progress in simple terms."
