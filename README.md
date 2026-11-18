# TaskSunIntern

FastAPI project with Core Setup and SQLite database.

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m alembic upgrade head
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs

## Test

```powershell
pytest -q
```

## Database

The project uses SQLite with async SQLAlchemy and Alembic migrations.
Task CRUD endpoints are available at `/tasks`.
