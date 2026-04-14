from openai import OpenAI
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.models import AssistantConversation, AssistantMessage, LearningProgress, User, WatchlistItem
from app.services.market_data_service import market_data_service
from app.services.portfolio_service import calculate_portfolio_value


class AIService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None

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

    def market_summary(self, overview: dict) -> str:
        prompt = f"Summarize this market data for beginners in 3 bullet points: {overview}"
        return self._complete(prompt, "Markets are mixed today. Focus on diversification and risk management.")

    def explain_news(self, headline: str, description: str) -> str:
        prompt = f"Explain this news in simple language:\nHeadline: {headline}\nDetails: {description}"
        return self._complete(prompt, "This headline may impact investor sentiment and short-term price moves.")

    def generate_quiz_question(self, lesson_title: str) -> dict:
        prompt = (
            "Create one beginner multiple-choice question as JSON with keys question, options (4), "
            f"correct_option, explanation about: {lesson_title}"
        )
        fallback = {
            "question": f"What is a core idea in {lesson_title}?",
            "options": ["Ignore risk", "Diversify", "Use only one stock", "Never review positions"],
            "correct_option": "Diversify",
            "explanation": "Diversification helps reduce single-asset risk."
        }
        text = self._complete(prompt, str(fallback))
        try:
            import json

            return json.loads(text)
        except Exception:
            return fallback

    def _generate_answer(self, db: Session, user: User, question: str, page: str | None) -> str:
        portfolio_value = calculate_portfolio_value(db, user)
        watch_count = db.query(WatchlistItem).filter_by(user_id=user.id).count()
        completed = db.query(LearningProgress).filter_by(user_id=user.id, completed=True).count()
        market = market_data_service.market_overview()

        prompt = (
            "You are SimpleTrade AI coach. Keep answers concise and beginner-friendly.\n"
            f"Page: {page}\n"
            f"User cash: {user.cash_balance}\nPortfolio value: {portfolio_value}\n"
            f"Watchlist items: {watch_count}\nCompleted lessons: {completed}\n"
            f"Market snapshot: {market}\n"
            f"User question: {question}"
        )
        return self._complete(prompt, self._fallback_answer(question, user, portfolio_value, watch_count, completed))

    def _complete(self, prompt: str, fallback: str) -> str:
        if not self.client:
            return fallback
        try:
            response = self.client.responses.create(
                model="gpt-4.1-mini",
                input=prompt,
                temperature=0.4,
            )
            text = response.output_text
            return text.strip() if text else fallback
        except Exception:
            return fallback

    def _fallback_answer(self, question: str, user: User, value: float, watch_count: int, completed: int) -> str:
        q = question.lower()
        if "portfolio" in q:
            return f"Your portfolio is around ${value:,.2f} with ${user.cash_balance:,.2f} cash."
        if "watchlist" in q:
            return f"You track {watch_count} assets. Consider balancing sectors and risk levels."
        if "study" in q or "lesson" in q:
            return f"You completed {completed} lessons. Next focus: risk management and diversification."
        if "market" in q:
            return "Market is mixed today. Stay diversified and size positions carefully."
        return "Ask me about your portfolio, watchlist, market, or what to study next."


ai_service = AIService()
