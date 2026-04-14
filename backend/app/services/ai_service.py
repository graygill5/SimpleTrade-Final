from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.models import AssistantConversation, AssistantMessage, LearningProgress, User, WatchlistItem
from app.services.market_service import get_market_overview
from app.services.portfolio_service import calculate_portfolio_value


class AIService:
    def ask(self, db: Session, user: User, question: str, page: str | None = None) -> dict:
        convo = db.query(AssistantConversation).filter_by(user_id=user.id).order_by(AssistantConversation.id.desc()).first()
        if not convo:
            convo = AssistantConversation(user_id=user.id)
            db.add(convo)
            db.commit()
            db.refresh(convo)

        db.add(AssistantMessage(conversation_id=convo.id, role="user", content=question))
        answer = self._generate_answer(db, user, question, page)
        db.add(AssistantMessage(conversation_id=convo.id, role="assistant", content=answer))
        db.commit()
        return {"answer": answer, "conversation_id": convo.id}

    def _generate_answer(self, db: Session, user: User, question: str, page: str | None) -> str:
        # TODO: integrate real OpenAI call when OPENAI_API_KEY is set.
        if settings.openai_api_key:
            return "OpenAI integration placeholder: wire model call in services/ai_service.py"

        q = question.lower()
        if "portfolio" in q:
            total = calculate_portfolio_value(db, user)
            return f"Your portfolio is about ${total:,.2f}. Cash is ${user.cash_balance:,.2f}."
        if "watchlist" in q:
            count = db.query(WatchlistItem).filter_by(user_id=user.id).count()
            return f"You have {count} watchlist assets. Want a quick risk breakdown?"
        if "study" in q or "lesson" in q:
            completed = db.query(LearningProgress).filter_by(user_id=user.id, completed=True).count()
            return f"You completed {completed} lessons. Next: risk management and diversification." 
        if "market" in q:
            overview = get_market_overview()
            return f"Market summary: {overview['summary']} Top mover: {overview['top_gainers'][0]['symbol']}."
        return f"SimpleTrade coach here. On {page or 'this page'}, ask me about portfolio, market, or learning progress."


ai_service = AIService()
