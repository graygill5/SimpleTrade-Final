# SimpleTrade (MVP)

SimpleTrade is a login-required social trading, market-learning, and paper-investing platform.

## Stack
- Frontend: **Next.js + TypeScript + Tailwind**
- Backend: **FastAPI (Python)**
- Database: **PostgreSQL**
- ORM: **SQLAlchemy**
- Migrations: **Alembic**
- Realtime: **WebSockets**

## MVP Included
- Public pages: landing, login, signup.
- Authenticated dashboard with sidebar + top search + persistent AI assistant widget.
- Main app pages:
  - Market Overview (search, detail view, watchlist)
  - Community Chat (rooms + realtime messages + typing + presence signals)
  - Portfolio (paper trading engine, holdings, PnL summary, allocation chart)
  - Learning Modules (modules, completion, XP/level/currency rewards)
- Social layer MVP:
  - user search
  - friend requests + accept
  - close friend toggle
  - close-friend read-only portfolio endpoint
- Notifications endpoint MVP.
- AI assistant endpoint with fallback mock orchestration and per-user history persistence.
- Seed data with demo users and starter rooms/modules.

## Demo Credentials
- `demo@simpletrade.dev` / `demo1234`
- `joe@simpletrade.dev` / `demo1234`

## Project Structure
```
backend/
  app/
    api/
    core/
    db/
    models/
    schemas/
    services/
    utils/
  alembic/
frontend/
  app/
  components/
  lib/
```

## Quick Start

### 1) Start PostgreSQL
```bash
docker compose up -d postgres
```

### 2) Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp ../.env.example .env
alembic upgrade head
python -m app.utils.seed
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

> For quick MVP boot, the app startup also runs `Base.metadata.create_all()` and seeds core data.

### 3) Frontend
```bash
cd frontend
npm install
cp ../.env.example .env.local
npm run dev
```

- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API docs: http://localhost:8000/docs

## Migrations
- Current migration file: `backend/alembic/versions/0001_initial.py`
- Generate next migration:
```bash
cd backend
alembic revision --autogenerate -m "describe change"
alembic upgrade head
```

## Seed Data
Seed logic lives in `backend/app/utils/seed.py` and is executed at startup.

## Architecture Notes
- Business logic is centralized in Python services (`services/`).
- Market data is mock/provider-ready and easy to swap with real APIs later.
- AI assistant uses a dedicated service with OpenAI-key-aware fallback logic.
- Chat, portfolios, learning, rewards, and assistant messages all persist in PostgreSQL.

## Next Iteration Suggestions
- refresh-token rotation + revoke endpoints
- richer direct/group messaging permissions
- unread counters + moderation actions
- deeper charts/performance history
- full quiz attempts/review UI
- real market/news data provider adapters
