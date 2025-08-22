# Backend (FastAPI)

See `backend/README.md` for full details.

## Quick Start (Docker)
- Copy env file: `cp backend/env.example backend/.env.local`
- Start stack: `docker compose up --build`
- API: http://localhost:8000 (docs at /docs)

## Quick Start (Local)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp env.example .env.local
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

## Notes
- With root Docker Compose, set `DB_HOST=postgres` and `REDIS_HOST=redis`.
- Migrations run at container start via `entrypoint.sh`.
