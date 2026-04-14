# SimpleTrade MVP

SimpleTrade is a login-required social trading and market learning app.

## Tech Stack
- Frontend: Next.js + TypeScript + Tailwind
- Backend: FastAPI + SQLAlchemy + Alembic
- Database: PostgreSQL
- Realtime Chat: WebSockets
- Market Data: `yfinance`
- News: NewsAPI
- AI: OpenAI API

## What works end-to-end
- Signup/Login (JWT access + refresh)
- Market dashboard with ticker search, details, historical chart data from Yahoo Finance, NewsAPI headlines, and AI summary
- Watchlist add/remove
- Realtime chat channels (WebSocket)
- Paper trading (buy/sell, holdings, trade history, valuation from Yahoo prices)
- Learning modules, quiz flow, XP/levels/reward cash
- Persistent AI assistant widget with per-user chat history
- Friend requests + close-friend read-only portfolio endpoint

## 1) Configure environment
Copy `.env.example` to backend `.env` and frontend `.env.local` and set your keys:
- `DATABASE_URL`
- `JWT_SECRET_KEY`
- `OPENAI_API_KEY`
- `NEWS_API_KEY`
- `NEXT_PUBLIC_API_BASE_URL`
- `BACKEND_CORS_ORIGINS`

## 2) Start PostgreSQL
```bash
docker compose up -d postgres
```

## 3) Backend setup
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp ../.env.example .env
```

Run migrations:
```bash
alembic upgrade head
```

Seed data:
```bash
python -m app.utils.seed
```

Start API (either command works):
```bash
# from repo root
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# or from backend/
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 4) Frontend setup
```bash
cd frontend
npm install
cp ../.env.example .env.local
npm run dev
```

Frontend: `http://localhost:3000`  
Backend: `http://localhost:8000`  
Docs: `http://localhost:8000/docs`

## Demo user
- `demo@simpletrade.dev` / `demo1234`

## Notes
- If `OPENAI_API_KEY` is missing, AI features fall back to deterministic local responses.
- If `NEWS_API_KEY` is missing, news falls back to mock headlines.
- Yahoo Finance integration (`yfinance`) is live by default.
