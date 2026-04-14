from datetime import datetime, timedelta

import yfinance as yf

DEFAULT_TRACKED = ["^GSPC", "^IXIC", "^DJI", "AAPL", "MSFT", "NVDA", "SPY", "QQQ", "BTC-USD", "ETH-USD"]


class MarketDataService:
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
            "market_cap": float(info.get("market_cap") or 0),
            "outlook": "bullish" if change_pct > 1 else "bearish" if change_pct < -1 else "neutral",
            "why_this_matters": f"{symbol.upper()} moved {change_pct}% today, signaling current market sentiment.",
        }

    def history(self, symbol: str, period: str = "1mo", interval: str = "1d") -> list[dict]:
        hist = yf.Ticker(symbol).history(period=period, interval=interval)
        points = []
        for idx, row in hist.tail(60).iterrows():
            points.append(
                {
                    "time": idx.strftime("%Y-%m-%d"),
                    "open": round(float(row["Open"]), 2),
                    "high": round(float(row["High"]), 2),
                    "low": round(float(row["Low"]), 2),
                    "close": round(float(row["Close"]), 2),
                    "volume": int(row["Volume"]),
                }
            )
        return points

    def market_overview(self) -> dict:
        quotes = [q for q in [self.quote(s) for s in DEFAULT_TRACKED] if q]
        tradable = [q for q in quotes if not q["symbol"].startswith("^")]
        gainers = sorted(tradable, key=lambda x: x["change_pct"], reverse=True)[:5]
        losers = sorted(tradable, key=lambda x: x["change_pct"])[:5]

        indexes = [q for q in quotes if q["symbol"].startswith("^")][:3]
        return {
            "indexes": indexes,
            "trending": tradable[:5],
            "top_gainers": gainers,
            "top_losers": losers,
            "updated_at": datetime.utcnow().isoformat(),
            "date_window": {
                "from": (datetime.utcnow() - timedelta(days=30)).date().isoformat(),
                "to": datetime.utcnow().date().isoformat(),
            },
        }


market_data_service = MarketDataService()
