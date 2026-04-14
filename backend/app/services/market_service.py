from datetime import datetime, timedelta

import requests
import yfinance as yf

from app.core.config import settings

DEFAULT_TRACKED = ["^GSPC", "^IXIC", "^DJI", "AAPL", "MSFT", "NVDA", "SPY", "QQQ", "BTC-USD", "ETH-USD"]


class MarketService:
    base_news_url = "https://newsapi.org/v2"

    def search(self, query: str) -> list[dict]:
        query = query.upper().strip()
        symbols = [s for s in DEFAULT_TRACKED if query in s]
        if query and query not in symbols:
            symbols = [query] + symbols
        return [self.quote(sym) for sym in symbols[:10] if self.quote(sym)]

    def quote(self, symbol: str) -> dict | None:
        t = yf.Ticker(symbol)
        info = t.fast_info
        if not info:
            return None
        last = float(info.get("last_price") or 0)
        prev = float(info.get("previous_close") or last or 1)
        change = round(last - prev, 2)
        change_pct = round((change / prev) * 100, 2) if prev else 0
        return {
            "symbol": symbol.upper(),
            "name": info.get("shortName") or symbol.upper(),
            "price": round(last, 2),
            "change": change,
            "change_pct": change_pct,
            "volume": int(info.get("last_volume") or 0),
            "outlook": "bullish" if change_pct > 1 else "bearish" if change_pct < -1 else "neutral",
            "why_this_matters": f"{symbol.upper()} moved {change_pct}% today, signaling current market sentiment.",
        }

    def history(self, symbol: str, period: str = "1mo", interval: str = "1d") -> list[dict]:
        hist = yf.Ticker(symbol).history(period=period, interval=interval)
        return [
            {
                "time": idx.strftime("%Y-%m-%d"),
                "close": round(float(row["Close"]), 2),
                "volume": int(row["Volume"]),
            }
            for idx, row in hist.tail(60).iterrows()
        ]

    def market_overview(self) -> dict:
        quotes = [q for q in [self.quote(s) for s in DEFAULT_TRACKED] if q]
        tradable = [q for q in quotes if not q["symbol"].startswith("^")]
        return {
            "indexes": [q for q in quotes if q["symbol"].startswith("^")][:3],
            "trending": tradable[:5],
            "top_gainers": sorted(tradable, key=lambda x: x["change_pct"], reverse=True)[:5],
            "top_losers": sorted(tradable, key=lambda x: x["change_pct"])[:5],
            "updated_at": datetime.utcnow().isoformat(),
        }

    def top_market_headlines(self) -> list[dict]:
        return self._news("business")

    def ticker_news(self, ticker: str) -> list[dict]:
        return self._news(f"{ticker} stock market", ticker=ticker)

    def _news(self, query: str, ticker: str = "market") -> list[dict]:
        if not settings.news_api_key:
            return self._fallback_news(ticker)
        path = "top-headlines" if query == "business" else "everything"
        params = {"apiKey": settings.news_api_key, "language": "en", "pageSize": 10}
        if path == "top-headlines":
            params["category"] = "business"
        else:
            params["q"] = query
            params["sortBy"] = "publishedAt"
        res = requests.get(f"{self.base_news_url}/{path}", params=params, timeout=15)
        res.raise_for_status()
        rows = res.json().get("articles", [])
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

    def _fallback_news(self, ticker: str) -> list[dict]:
        now = datetime.utcnow()
        return [
            {
                "title": f"{ticker.upper()} stays active as investors assess macro data",
                "source": "SimpleTrade Mock Feed",
                "description": "Add NEWS_API_KEY for live headlines.",
                "published_at": now.isoformat(),
                "url": "https://newsapi.org",
            },
            {
                "title": "Broader market mixed into the close",
                "source": "SimpleTrade Mock Feed",
                "description": "Fallback news item.",
                "published_at": (now - timedelta(hours=2)).isoformat(),
                "url": "https://newsapi.org",
            },
        ]


market_service = MarketService()
