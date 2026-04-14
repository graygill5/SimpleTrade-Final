import random

ASSETS = [
    {"symbol": "AAPL", "name": "Apple", "asset_type": "stock", "base": 212.0},
    {"symbol": "MSFT", "name": "Microsoft", "asset_type": "stock", "base": 425.0},
    {"symbol": "SPY", "name": "SPDR S&P 500 ETF", "asset_type": "etf", "base": 531.0},
    {"symbol": "QQQ", "name": "Invesco QQQ", "asset_type": "etf", "base": 447.0},
    {"symbol": "BTC", "name": "Bitcoin", "asset_type": "crypto", "base": 69500.0},
    {"symbol": "ETH", "name": "Ethereum", "asset_type": "crypto", "base": 3600.0},
    {"symbol": "NVDA", "name": "NVIDIA", "asset_type": "stock", "base": 980.0},
]


def _row(asset: dict) -> dict:
    price = round(asset["base"] * (1 + random.uniform(-0.02, 0.02)), 2)
    change_pct = round(random.uniform(-3.5, 3.5), 2)
    return {
        **asset,
        "price": price,
        "change_pct": change_pct,
        "volume": random.randint(1_000_000, 150_000_000),
    }


def get_asset(symbol: str) -> dict | None:
    for asset in ASSETS:
        if asset["symbol"] == symbol.upper():
            row = _row(asset)
            row["why_this_matters"] = f"{row['symbol']} influences sentiment in {row['asset_type']} markets."
            row["outlook"] = "bullish" if row["change_pct"] > 1 else "bearish" if row["change_pct"] < -1 else "neutral"
            return row
    return None


def search_assets(query: str) -> list[dict]:
    q = query.lower()
    return [_row(a) for a in ASSETS if q in a["symbol"].lower() or q in a["name"].lower()][:10]


def get_market_overview() -> dict:
    rows = [_row(a) for a in ASSETS]
    top_gainers = sorted(rows, key=lambda x: x["change_pct"], reverse=True)[:3]
    top_losers = sorted(rows, key=lambda x: x["change_pct"])[:3]
    return {
        "indexes": [
            {"name": "S&P 500", "symbol": "SPX", "change_pct": round(random.uniform(-1, 1), 2)},
            {"name": "NASDAQ", "symbol": "NDX", "change_pct": round(random.uniform(-1.5, 1.5), 2)},
            {"name": "Dow", "symbol": "DJI", "change_pct": round(random.uniform(-1, 1), 2)},
        ],
        "top_gainers": top_gainers,
        "top_losers": top_losers,
        "trending": random.sample(rows, k=min(5, len(rows))),
        "summary": "Markets are mixed as traders balance earnings optimism with rate-cut uncertainty.",
        "news": [
            {
                "headline": "Tech lifts broader indexes",
                "summary": "Mega-cap tech outperformed into the close.",
                "outlook": "bullish",
            },
            {
                "headline": "Crypto pulls back after rally",
                "summary": "Profit taking hit major coins intraday.",
                "outlook": "neutral",
            },
        ],
    }
