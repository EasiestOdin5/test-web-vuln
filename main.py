import os
import sqlite3
from fastapi import FastAPI
from fastapi import Request
from fastapi import Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
from database import verify_password, DB_PATH


load_dotenv()

app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key=os.environ["LAB_SESSION_SECRET"],
    same_site="lax",
    https_only=False,  # Local HTTP lab only
    max_age=1800
)


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <body>
            <h1>Security Lab</h1>
            <p>FastAPI is running.</p>
            <a href="/login">Login</a>
        </body>
    </html>
    """


@app.get("/login", response_class=HTMLResponse)
def login():
    return """
    <h2>Login</h2>
    <form method="post" action="/login">
        <input name="username" placeholder="Username">
        <input name="password" type="password" placeholder="Password">
        <button type="submit">Login</button>
    </form>
    """


@app.post("/login")
def authenticate(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    # Retrieve user from database
    with sqlite3.connect(DB_PATH) as conn:
        user = conn.execute(
            """
            SELECT id, username, role, password_hash
            FROM users
            WHERE username = ?
            """,
            (username,)
        ).fetchone()

    # Verify password
    if not user or not verify_password(password, user[3]):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    # Clear any previous session
    request.session.clear()

    # Store authenticated user ID
    request.session["user_id"] = user[0]

    # Redirect to dashboard
    return RedirectResponse(
        url="/dashboard",
        status_code=303
    )


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    user_id = request.session.get("user_id")

    if user_id is None:
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    return HTMLResponse(
        "<h2>Dashboard</h2>"
        f"<p>Authenticated user ID: {user_id}</p>"
    )
