## Architecture Overview

This repository demonstrates production-grade backend practices while redacting proprietary business logic. The code is organized using layered architecture with clear boundaries:

- Application layer (`src/application`): Orchestrates use-cases and coordinates domain and infrastructure.
- Domain layer (`src/domain`): Core entities, models, and domain-specific services.
- Infrastructure layer (`src/infrastructure`): Integrations (email, LLM, news providers, Redis, Celery, websockets) behind clean interfaces.
- API layer (`src/routers`): FastAPI routers exposing HTTP and WebSocket endpoints.
- Config (`config/`): Settings, middleware, exception/response handling, DB connection.

### Key Patterns
- Dependency inversion for external services (e.g., news fetchers implement `NewsFetcherBase`).
- Environment-driven configuration with `.env.<environment>` files and `pydantic-settings`.
- Unified error handling via `BaseHTTPException` and `ResponseHandler`.
- Background processing with Celery; real-time notifications via Redis and websockets.
- Testability through clear interfaces and a lightweight test scaffold.

### Request Flow
1. Client hits a route under `/api/v1/*`.
2. Middleware assigns a request id and handles global concerns.
3. Router delegates to application services, which call domain and infrastructure.
4. Responses are standardized via `ResponseHandler`.
5. Errors are surfaced through `BaseHTTPException` and exception handlers.

### Redaction Strategy
- No hard-coded secrets or API keys; all integrations are configured via env vars.
- Example integrations are provided with safe defaults and can be easily stubbed for demos/tests.

### Extensibility
- Add new integrations by implementing an interface in `src/infrastructure/*/core/` and wiring through the application layer.
- Add new endpoints as routers under `src/routers/` and include them in `src/main.py`.


