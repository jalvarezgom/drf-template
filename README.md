# DRFTemplate

Base template for building APIs with Django + Django REST Framework. It is designed both as a starting point for new projects and as an onboarding guide: it includes environment-based configuration, custom authentication, background task support, reusable managers for external services, and shared utilities.

## Key features

- OpenAPI schema via `drf-spectacular`
- Custom authentication: secret key and expiring tokens in `apps/authentication` (backends and authenticators)
- Background tasks: Celery support with `django-celery-beat` and `django-celery-results`
- Reusable managers: Gmail (OAuth) and S3 in `apps/core/managers` to isolate external integrations
- Environment-based configuration: `config/environment.py` centralizes runtime mode, settings loading, and rotating logger setup
- Shared utilities: pagination, validators, base serializers, and an extended router (`apps/core`)

## Project structure

- `config/` — environment settings (`config/settings/*`), URLs, and `config/environment.py`
- `apps/` — domain apps: `authentication`, `task`, `app_1`, `app_2`, `app_3`, `core`
- `pyproject.toml` — dependencies and PDM scripts (`cold_start`, `seeder`, `lint`, `test`)
- `.env.example` — expected environment variables

## Technical details and conventions

- `AUTH_USER_MODEL` points to `authentication.User`
- `REST_FRAMEWORK` uses `drf-spectacular`; default permissions require authentication and model permissions
- Included backends: `email_password.EmailPasswordBackend` and `secret_key.SecretKeyBackend`
- Logging is split between `config/loggers/dev.py` and `config/loggers/pro.py`, and applied through `Environment`

## Scripts and tools (PDM)

Run with `pdm run <script>` (or adapt to your package manager):

- `cold_start` — `makemigrations`, `migrate`, `seeder` (boots a local DB with demo data)
- `seeder` — runs the project's `manage.py seeder` command
- `lint` — `ruff check --fix` + `ruff format`
- `test` — runs `pytest` (configured to use `config.settings.test`)

## Quick start (local)

1. Copy `.env.example` to `.env.dev` and fill in values (DB, SECRET_KEY, EMAIL, S3, REDIS, etc.).
2. Install dependencies: `pdm install` or `pip install -r requirements.txt`.
3. Run migrations: `python manage.py migrate`.
4. Load initial data: `pdm run seeder` or `python manage.py seeder`.
5. Start the server: `python manage.py runserver`.

## Onboarding a new project

1. Rename the project and update `APP_NAME`, `ENV`, and `SECRET_KEY`.
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

- `config/environment.py` defines runtime modes (API, TASK, DJANGO, TEST) and selects settings (dev/test/pro)
- See `.env.example` for critical variables: `ENV`, `APP_NAME`, `SECRET_KEY`, `DB__*`, `EMAIL__*`, `S3__*`, `REDIS__*`, `TOKEN_EXPIRED_AFTER_SECONDS`

## What to customize first

- Project name and `APP_NAME`
- Environment variables
- Database and credentials
- Allowed CORS origins and domains
- Optional integrations: email, S3, Redis, and Celery
- Apps and endpoints you will actually use

## Where to look first

- `config/environment.py` — runtime behavior and logger setup
- `config/settings/base.py` — DRF behavior and authentication
- `config/urls.py` — router mounting and documentation routes
- `apps/authentication/` — users, backends, authenticators, and auth views
- `apps/core/` — pagination, extended router, and managers
