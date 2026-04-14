from datetime import datetime, timedelta

import requests

from app.core.config import settings


class NewsService:
    base_url = "https://newsapi.org/v2"

    def top_market_headlines(self) -> list[dict]:
        if not settings.news_api_key:
            return self._fallback()
        params = {
            "category": "business",
            "language": "en",
            "pageSize": 10,
            "apiKey": settings.news_api_key,
        }
        res = requests.get(f"{self.base_url}/top-headlines", params=params, timeout=15)
        res.raise_for_status()
        return self._normalize(res.json().get("articles", []))

    def ticker_news(self, ticker: str) -> list[dict]:
        if not settings.news_api_key:
            return self._fallback(ticker)
        params = {
            "q": f"{ticker} stock market",
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": 10,
            "apiKey": settings.news_api_key,
        }
        res = requests.get(f"{self.base_url}/everything", params=params, timeout=15)
        res.raise_for_status()
        return self._normalize(res.json().get("articles", []))

    def _normalize(self, rows: list[dict]) -> list[dict]:
        return [
            {
                "title": r.get("title", ""),
                "source": (r.get("source") or {}).get("name", ""),
                "description": r.get("description", ""),
                "published_at": r.get("publishedAt", ""),
                "url": r.get("url", ""),
            }
            for r in rows
        ]

    def _fallback(self, ticker: str = "market") -> list[dict]:
        now = datetime.utcnow().isoformat()
        return [
            {
                "title": f"{ticker.upper()} stays active as investors assess macro data",
                "source": "SimpleTrade Mock Feed",
                "description": "Add NEWS_API_KEY for live NewsAPI headlines.",
                "published_at": now,
                "url": "https://newsapi.org",
            },
            {
                "title": "Broader market mixed into the close",
                "source": "SimpleTrade Mock Feed",
                "description": f"Generated fallback headline for {ticker.upper()} context.",
                "published_at": (datetime.utcnow() - timedelta(hours=2)).isoformat(),
                "url": "https://newsapi.org",
            },
        ]


news_service = NewsService()
