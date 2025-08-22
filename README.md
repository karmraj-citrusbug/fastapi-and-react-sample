# FastAPI + React Sample (Monorepo)

A full‑stack sample with a FastAPI backend and a React (CRA + TypeScript) frontend. Includes Docker/Docker Compose for local development and production‑like runs, Celery workers, Redis, and Postgres.

---

## Stack
- **Backend**: FastAPI, SQLAlchemy, Alembic, Celery
- **Frontend**: React 18, CRA, TypeScript
- **Infra**: Postgres 15, Redis 7, Docker Compose

---

## Quick Start (Docker)

1) Copy backend environment file and adjust values:
```bash
cp backend/env.example backend/.env.local
```

2) Start the full stack:
```bash
docker compose up --build
```

Services:
- API: http://localhost:8000 (docs at /docs)
- Frontend: http://localhost:3000
- Postgres: localhost:5432
- Redis: localhost:6379

Stop stack:
```bash
docker compose down
```

---

## Local Development (without Docker)

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
cp env.example .env.local
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend
```bash
cd frontend
npm ci
npm start
```

---

## Docker Compose Layout
The root `docker-compose.yml` builds/starts:
- `postgres`: Postgres 15 with volume `pg-data`
- `redis`: Redis 7 with volume `redis-data`
- `backend`: FastAPI app on port 8000
- `celery-worker`: Celery worker using backend code
- `celery-beat`: Celery beat scheduler
- `frontend`: React dev server on port 3000

Notes:
- Backend services get DB and Redis hosts injected as `postgres` and `redis` respectively.
- The backend uses environment files like `backend/.env.local` selected via `ENVIRONMENT` (defaults to `local`).

---

## Environment Configuration

Backend variables live in `backend/.env.<environment>`.
Copy from `backend/env.example` and adjust:
```bash
cp backend/env.example backend/.env.local
```
Important keys:
- `DB_HOST` should be `postgres` when using root Docker Compose.
- `REDIS_HOST` should be `redis` when using root Docker Compose.
- `CORS_ALLOWED_ORIGINS` should include `http://localhost:3000` for local UI.

---

## Migrations
Alembic runs during backend image build, and can be run manually:
```bash
cd backend
alembic upgrade head
```

---

## Useful Commands
- Rebuild only backend:
```bash
docker compose build backend && docker compose up backend
```
- Tail logs:
```bash
docker compose logs -f backend celery-worker celery-beat frontend
```
- Remove containers/volumes:
```bash
docker compose down -v
```

---

## Repository Layout
```
backend/   # FastAPI app, Celery, Alembic, tests
frontend/  # React app (CRA + TypeScript)
```

For deeper backend details, see `backend/README.md`.
