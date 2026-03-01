Plantilla DRF — DRFTemplate
===========================

Proyecto arquetipo para construir APIs con Django + Django REST Framework. Integra soluciones y decisiones prácticas que facilitan arrancar proyectos productivos: configuración por entornos, autenticación personalizada, JSON:API, tareas en background, managers para servicios externos y utilidades comunes.

Principales características
- Esquema OpenAPI mediante `drf-spectacular`
- Autenticación personalizada: secret-key y tokens con expiración en `apps/authentication` (backends y autenticadores).
- Tareas en background: soporte Celery + `django-celery-beat` y `django-celery-results`.
- Managers reutilizables: Gmail (OAuth) y S3 en `apps/core/managers` para aislar integraciones externas.
- Configuración por entorno: `config/environment.py` centraliza modo de ejecución, carga de settings y logger rotativo.
- Utilidades compartidas: paginaciones, validadores, serializers base y router extendido (`apps/core`).

Estructura relevante
- `config/` — settings por entorno (`config/settings/*`), URLs y `config/environment.py`.
- `apps/` — apps del dominio: `authentication`, `task`, `app_1`, `app_2`, `app_3`, `core`.
- `pyproject.toml` — dependencias y scripts PDM (`cold_start`, `seeder`, `lint`, `test`).
- `.env.example` — variables de entorno esperadas.

Detalles técnicos y convenciones
- `AUTH_USER_MODEL` apunta a `authentication.User`.
- `REST_FRAMEWORK` usa `JsonApiAutoSchema` y renderers/parsers de JSON:API; permisos por defecto requieren autenticación y permisos de modelo.
- Backends incluidos: `email_password.EmailPasswordBackend` y `secret_key.SecretKeyBackend`.
- Logging: configuraciones separadas en `config/loggers/dev.py` y `config/loggers/pro.py`, aplicadas por `Environment`.

Scripts y herramientas (PDM)
- Ejecutar con `pdm run <script>` (o adapta a tu gestor):
  - `cold_start` — `makemigrations`, `migrate`, `seeder` (inicia DB local con datos demo).
  - `seeder` — ejecuta el comando `manage.py seeder` del proyecto.
  - `lint` — `ruff check --fix` + `ruff format`.
  - `test` — ejecuta `pytest` (configurado para usar `config.settings.test`).

Inicio rápido (local)
1) Copia `.env.example` a `.env.dev` y completa valores (DB, SECRET_KEY, EMAIL, S3, REDIS, etc.).
2) Instala dependencias: `pdm install` o `pip install -r requirements.txt`.
3) Ejecuta migraciones: `python manage.py migrate`.
4) Población inicial: `pdm run seeder` o `python manage.py seeder`.
5) Levanta servidor: `python manage.py runserver`.

Ejecución y mantenimiento de Celery
- Worker: `celery -A config worker -l INFO` (ajusta broker y backend en `.env`).
- Beat: `celery -A config beat -l INFO` o usar `django-celery-beat` desde el admin para programar tareas.

Pruebas y calidad
- Tests: `pdm run test` o `pytest`.
- Lint/format: `pdm run lint`.

Configuración por entorno y variables
- `config/environment.py` define modos (API, TASK, DJANGO, TEST) y selecciona settings (dev/test/pro).
- Revisa `.env.example` para variables críticas: `ENV`, `APP_NAME`, `SECRET_KEY`, `DB__*`, `EMAIL__*`, `S3__*`, `REDIS__*`, `TOKEN_EXPIRED_AFTER_SECONDS`.

Dónde mirar primero
- `config/environment.py` — comportamiento del entorno y logger.
- `config/settings/base.py` — comportamiento DRF/JSON:API y autenticación.
- `config/urls.py` — montaje de routers y rutas de documentación.
- `apps/authentication/` — usuarios, backends, autenticadores y vistas de auth.
- `apps/core/` — paginaciones, router extendido y managers.

