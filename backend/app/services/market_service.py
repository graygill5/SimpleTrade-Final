import random

MOCK_PRICES = {
    "AAPL": 212.33,
    "MSFT": 428.11,
    "NVDA": 976.15,
    "TSLA": 201.78,
    "SPY": 531.91,
}


def get_price(symbol: str) -> float:
    base = MOCK_PRICES.get(symbol.upper(), 100.0)
    return round(base + random.uniform(-2.5, 2.5), 2)


def market_snapshot() -> list[dict]:
    return [
        {
            "symbol": symbol,
            "price": get_price(symbol),
            "change_pct": round(random.uniform(-2.5, 2.5), 2),
            "plain_english": f"{symbol} is moving with moderate volatility.",
        }
        for symbol in MOCK_PRICES
    ]


def market_news() -> list[dict]:
    return [
        {
            "headline": "Tech leads midday rebound",
            "summary": "Large-cap tech names are pushing indices higher.",
            "ai_summary": "Investors are rotating back into growth stocks after inflation concerns cooled.",
        },
        {
            "headline": "Energy stocks lag as oil cools",
            "summary": "Crude prices eased, reducing momentum in energy shares.",
            "ai_summary": "Lower energy prices can help inflation but may pressure oil-heavy portfolios.",
        },
    ]
