# FastAPI Backend Template

A production-ready FastAPI backend template demonstrating clean architecture, environment-driven configuration, background processing, and real-time capabilities.

---

## Features
- **Authentication-ready**: JWT-based patterns for auth flows
- **CRUD scaffolding**: Example structure for request/response schemas and services
- **Background tasks**: Celery integration for scheduled/async jobs
- **Real-time**: WebSocket support for live updates
- **Configurable**: Environment-based settings via `.env.<environment>`
- **Resilient**: Centralized exception handling and standardized API responses
- **Observability**: Structured logging with request IDs
- **Production Ready**: Docker, Docker Compose, Alembic migrations

---

## Directory Structure
```
backend/
├── alembic/                # Database migrations
├── config/                 # App configuration, middleware, settings
├── src/
│   ├── application/        # Use-cases and orchestration
│   ├── domain/             # Models, enums, and domain services
│   ├── exceptions/         # Custom exception classes/handlers
│   ├── infrastructure/     # Integrations (email, LLM, websockets, tasks)
│   ├── routers/            # FastAPI routers (API endpoints)
│   ├── schema/             # Pydantic schemas
│   ├── main.py             # FastAPI app entrypoint
│   └── celery_worker.py    # Celery worker entrypoint
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## Getting Started

### 1. Install Dependencies (local)
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Environment Configuration
Copy `env.example` to `.env.local` (or `.env.prod`) and adjust values:
```bash
cp env.example .env.local
```
Environment is auto-selected via `ENVIRONMENT`.

---

## Run

### Local Development
```bash
python -m uvicorn --host 0.0.0.0 src.main:app --reload
```

### With Docker
Build and run all services (API, Celery, Redis):
```bash
docker compose --env-file .env.local up --build
```
For production:
```bash
docker compose --env-file .env.prod up --build -d
```

---

## Database Migrations
- Alembic is used for migrations.
- Run manually:
```bash
alembic upgrade head
```

---

## Background Tasks (Celery)
- Celery worker and beat are included in Docker Compose.
- Tasks are defined under `src/infrastructure/tasks.py`.

---

## API Overview
- All endpoints are under `/api/v1/` (by convention)
- Interactive docs available at `/docs` in non-production environments
- Health check: `/api/v1/health`

---

## Security & Best Practices
- Use strong, unique secrets for JWT, DB, and API keys
- Never commit secrets to version control
- Use `.env.*` files for environment-specific config
- Configure CORS via environment variables
- Pin dependencies in `requirements.txt`
- Use Docker for consistent, reproducible builds
- Run with `DEBUG=false` in non-local environments
- Keep dependencies updated and patched

---

## Development Hygiene
- Set up pre-commit hooks:
  ```bash
  pre-commit install
  pre-commit run -a
  ```
- Run tests:
  ```bash
  pytest -q
  ```

