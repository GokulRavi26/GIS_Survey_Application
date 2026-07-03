# GIS Survey Application Backend

FastAPI backend for the GIS Survey Application.

## Module 1: Backend Foundation

Implemented foundation components:

- FastAPI application factory entrypoint through `app.main:app`
- Environment-backed configuration from `server/.env`
- SQLite database connection with SQLAlchemy 2 style engine/session
- Database directory, upload directory, export directory, and log directory setup
- Alembic migration scaffolding
- Structured console and rotating file logging
- Versioned API router under `/api/v1`
- Health API with database connectivity check
- Swagger documentation at `/docs`
- ReDoc documentation at `/redoc`
- Root compatibility health endpoint at `/health`

## Folder Structure

```text
server/
  alembic/
    versions/
    env.py
    script.py.mako
  app/
    api/
      v1/
        health.py
        router.py
      auth.py
      users.py
      properties.py
      survey.py
      gallery.py
      reports.py
    core/
      config.py
      dependencies.py
      logging.py
      security.py
    database/
      base.py
      database.py
      init_db.py
      session.py
    models/
    repositories/
    schemas/
    services/
    utils/
    main.py
  database/
  exports/
  logs/
  uploads/
  .env.example
  alembic.ini
  main.py
  requirements.txt
```

## Environment Setup

Create `server/.env` from `server/.env.example` and set a strong `SECRET_KEY`.

Required environment variables:

```text
APP_NAME
APP_VERSION
SECRET_KEY
ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES
DEFAULT_ADMIN_NAME
DEFAULT_ADMIN_MOBILE
DEFAULT_ADMIN_PASSWORD
DEFAULT_ADMIN_ROLE
```

Optional foundation variables:

```text
ENVIRONMENT
DEBUG
API_V1_PREFIX
DATABASE_URL
DATABASE_CONNECT_TIMEOUT_SECONDS
LOG_LEVEL
LOG_FILE
BACKEND_CORS_ORIGINS
```

## Run Backend

```powershell
cd server
.\venv\Scripts\uvicorn.exe app.main:app --reload
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

Health:

```text
http://127.0.0.1:8000/api/v1/health
```

## Alembic

Generate a migration:

```powershell
cd server
.\venv\Scripts\alembic.exe revision --autogenerate -m "create initial tables"
```

Apply migrations:

```powershell
cd server
.\venv\Scripts\alembic.exe upgrade head
```

## Verification

```powershell
cd ..
server\venv\Scripts\python.exe -m compileall server\app
```

```powershell
cd server
.\venv\Scripts\python.exe -c "from app.main import app; print(app.title)"
```
