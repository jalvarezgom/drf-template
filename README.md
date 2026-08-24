# DRFTemplate

Base template for building APIs with Django + Django REST Framework. It is designed both as a starting point for new projects and as an onboarding guide: it includes environment-based configuration, custom authentication, background task support, reusable managers for external services, and shared utilities.

## Key features

- OpenAPI schema via `drf-spectacular`
- Custom authentication: secret key and expiring tokens in `apps/authentication` (backends and authenticators), with rate limiting on the secret-key backend and dedicated throttle scopes for login/register/recover-password/OTP (`apps/authentication/throttling.py`)
- Request/response tracing: two independent middlewares (`apps/core/middlewares/request_logging.py`, `response_logging.py`) log every incoming request and outgoing response, correlated by a `django_guid` correlation id; toggle with `APP__LOG_REQUESTS`/`APP__LOG_RESPONSES`
- Background tasks: Celery support with `django-celery-beat` and `django-celery-results`
- Reusable managers: Gmail (OAuth) and S3 in `apps/core/managers` to isolate external integrations
- Environment-based configuration: `config/environment.py` centralizes runtime mode, settings loading, and rotating logger setup; the active environment (`dev`/`prod`/`test`) is selected from the OS-level `ENV` variable
- Shared utilities: pagination, validators, base serializers, and an extended router (`apps/core`)

## Project structure

- `config/` — environment settings (`config/settings/*`, incl. `dev.py`/`prod.py`/`test.py`), URLs, loggers (`config/loggers/*`), and `config/environment.py`
- `apps/` — domain apps: `authentication`, `task`, `app_1`, `app_2`, `app_3`, `core`
- `apps/core/middlewares/` — request/response logging middlewares
- `apps/authentication/throttling.py` — DRF throttle scopes for sensitive auth endpoints
- `pyproject.toml` — dependencies and PDM scripts (`cold_start`, `seeder`, `lint`, `test`)
- `.env.example` — expected environment variables

## Technical details and conventions

- `AUTH_USER_MODEL` points to `authentication.User`
- `REST_FRAMEWORK` uses `drf-spectacular`; default permissions require authentication and model permissions; global anon/user throttling plus per-endpoint scopes for login/register/recover-password/OTP
- Included backends: `email_password.EmailPasswordBackend` and `secret_key.SecretKeyBackend` (rate-limited: 5 failed attempts per IP per 60s)
- `apps/authentication/middlewares/disable_csrf.py` only disables CSRF checks when running in dev mode (`Environment.is_dev_mode()`); it is not wired into `MIDDLEWARE` by default
- Logging is split between `config/loggers/dev.py` and `config/loggers/pro.py`, applied through `Environment`. Both define a `root` logger (so third-party loggers are never silently dropped), a shared formatter, and the `django_guid.log_filters.CorrelationId` filter — every log line, including Django's own `django.request`/`django.server`, carries the same correlation id as a given request. The rotated log file in `pro.py` keeps 30 days of history (`backupCount=30`)

## Scripts and tools (PDM)

Run with `pdm run <script>` (or adapt to your package manager):

- `cold_start` — `makemigrations`, `migrate`, `seeder` (boots a local DB with demo data)
- `seeder` — runs the project's `manage.py seeder` command
- `lint` — `ruff check --fix` + `ruff format`
- `test` — runs `pytest` (configured to use `config.settings.test`)

## Requirements

- Python >= 3.12
- PostgreSQL client libraries are bundled via `psycopg[binary]`; SQLite works out of the box for local development (`DB__ENGINE=django.db.backends.sqlite3`)

## Quick start (local)

1. Copy `.env.example` to `.env.dev` and fill in values (DB, `APP__SECRET_KEY`, EMAIL, S3, REDIS, etc.).
2. Install dependencies: `pdm install` or `pip install -r requirements.txt`.
3. Run migrations: `python manage.py migrate`.
4. Load initial data: `pdm run seeder` or `python manage.py seeder`.
5. Start the server: `python manage.py runserver`.

## Onboarding a new project

1. Rename the project and update `APP__NAME`, `ENV`, and `APP__SECRET_KEY`.
2. Review `config/settings/base.py` and define permissions, authentication, CORS, and active apps.
3. Fill out `.env.example` with only the variables your deployment will actually use.
4. Check `config/environment.py` to decide which external services are initialized.
5. Review `config/urls.py` and remove routes or apps you do not need.
6. Add your domain apps inside `apps/` and register their URLs, serializers, and tests.

## Celery

- Worker: `celery -A config worker -l INFO` (adjust broker and backend in `.env`)
- Beat: `celery -A config beat -l INFO` or use `django-celery-beat` from the admin to schedule tasks

## Testing and quality

- Tests: `pdm run test` or `pytest`
- Lint/format: `pdm run lint`

## Environment configuration and variables

- `config/environment.py` defines runtime modes (API, TASK, DJANGO, TEST) and selects settings (`dev`/`prod`/`test`). Which one loads is driven by the OS-level `ENV` variable (e.g. `ENV=PROD` set in the process/container, not inside `.env.prod`) — it must be set *before* the process starts, since it decides which `.env.<env>` file gets loaded in the first place. Defaults to `dev` if unset.
- App-level settings live under the `APP__*` prefix (`config/environs/base.py:EnvironSettingsApp`): `APP__NAME`, `APP__SECRET_KEY`, `APP__DEBUG`, `APP__FRONTEND_URL`, `APP__TOKEN_EXPIRED_AFTER_SECONDS`, `APP__ALLOWED_HOSTS` and `APP__CORS_ALLOWED_ORIGINS` (comma-separated, used in `prod.py` — `dev.py` stays permissive for local work), and `APP__LOG_REQUESTS`/`APP__LOG_RESPONSES` (toggle the tracing middlewares).
- See `.env.example` for the full list: `ENV`, `APP__*`, `DB__*`, `EMAIL__*`, `S3__*`, `REDIS__*`, `SENTRY__*`, `IA__*`, `AUDIT__*`

## What to customize first

- Project name and `APP__NAME`
- Environment variables
- Database and credentials
- `APP__ALLOWED_HOSTS` and `APP__CORS_ALLOWED_ORIGINS` for production (`config/settings/prod.py`)
- Optional integrations: email, S3, Redis, Sentry, and Celery
- Apps and endpoints you will actually use

## Where to look first

- `config/environment.py` — runtime behavior and logger setup
- `config/settings/base.py` — DRF behavior, authentication, and middleware wiring
- `config/loggers/` — logging configuration (dev/prod), correlation id filter
- `config/urls.py` — router mounting and documentation routes
- `apps/authentication/` — users, backends, authenticators, throttling, and auth views
- `apps/core/middlewares/` — request/response tracing middlewares
- `apps/core/` — pagination, extended router, and managers
