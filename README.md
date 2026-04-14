# SimpleTrade

SimpleTrade is a full-stack social paper-trading and learning platform.

## Stack
- **Backend:** FastAPI + SQLAlchemy + PostgreSQL + WebSockets
- **Frontend:** React (Vite + TypeScript)
- **Business logic in Python:** auth, portfolio engine, rewards/XP, AI assistant orchestration, market/news mocks, learning modules

## Features
### Authenticated pages
1. **Market Overview**
   - Mock ticker snapshots
   - Mock finance news + AI-friendly summaries
   - Plain-English market explanations
2. **Community Chat**
   - Realtime WebSocket global room foundation
   - Model support for friend requests, friendships, close-friend markers, and message rooms
3. **Portfolio**
   - Persistent paper trading
   - Buy/sell with virtual money
   - Holdings + trade history model and APIs
4. **Learning Modules**
   - Lesson modules + progress tracking
   - Quiz completion endpoint
   - XP + reward ledger that adds virtual cash for paper trading

### Persistent AI Assistant Widget
Appears in authenticated layout and calls `/assistant/ask` for simple-language answers about:
- portfolio cash status
- market context
- learning XP progress

## Project structure
```
SimpleTrade-Final/
  backend/
    app/
      api/
      core/
      db/
      models/
      schemas/
      services/
  frontend/
    src/
      components/
      context/
      pages/
      services/
      styles/
  .env.example
  docker-compose.yml
```

## Setup
### 1) Start PostgreSQL
```bash
docker compose up -d postgres
```

### 2) Backend setup
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp ../.env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3) Frontend setup
```bash
cd frontend
npm install
cp ../.env.example .env
npm run dev
```

Frontend runs at `http://localhost:5173`, backend at `http://localhost:8000`.

## API notes
- Auth token: Bearer JWT via `/api/v1/auth/login` or `/api/v1/auth/signup`
- Protected routes use `HTTPBearer`
- WebSocket endpoint: `ws://localhost:8000/api/v1/chat/ws/global`

## Next extension ideas
- Add direct messages, group membership, and friend-request endpoints
- Add market data/news provider adapters
- Add charting + performance comparisons with close friends
- Add richer AI workflows via LLM provider and function calling
- Add Alembic migrations and role-based permissions
