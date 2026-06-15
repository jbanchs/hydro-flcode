from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from app.core.config import SESSION_COOKIE_NAME, SESSION_COOKIE_SECURE, get_session_secret_key
from app.core.security_headers import SecurityHeadersMiddleware
from app.routers import web, api, health

app = FastAPI(title="HYDRO", version="0.1.0")
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(
    SessionMiddleware,
    secret_key=get_session_secret_key(),
    session_cookie=SESSION_COOKIE_NAME,
    https_only=SESSION_COOKIE_SECURE,
    same_site="lax",
    max_age=60 * 60 * 8,
)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(health.router)
app.include_router(web.router)
app.include_router(api.router)
