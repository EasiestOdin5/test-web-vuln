# FastAPI Web Vulnerability Lab

An educational, local-only FastAPI web application for learning authentication, web vulnerability analysis, and secure code review. Do not deploy this intentionally vulnerable training project to the public internet.

## Setup (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Generate a unique session secret:

```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

Replace the placeholder `LAB_SESSION_SECRET` value in the local `.env` with the generated secret.

```powershell
python database.py
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000 and visit the login page.

## Disposable demo accounts

- `alice` / `alice123` (user)
- `bob` / `bob123` (admin)

## Notes

- `.env`, `lab.db`, and `.venv` are intentionally not committed. Recreate them on each computer.
- The app uses signed cookie sessions, local HTTP, and fixed demo accounts. It is for training, not production.
- The database initialization prints password hashes for local inspection; do not use this behavior in production.
