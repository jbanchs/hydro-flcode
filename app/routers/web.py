import secrets

from fastapi import APIRouter, Form, Request, status
from fastapi.responses import PlainTextResponse
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.auth import current_user
from app.services.regulation_service import list_regulations
from app.services.auth_service import authenticate_user, generate_csrf_token

router = APIRouter(tags=["web"])
templates = Jinja2Templates(directory="app/templates")


def rotate_csrf_token(request: Request) -> str:
    csrf_token = generate_csrf_token()
    request.session["csrf_token"] = csrf_token
    return csrf_token


def is_valid_csrf_token(request: Request, csrf_token: str) -> bool:
    session_token = request.session.get("csrf_token")
    return bool(csrf_token and session_token and secrets.compare_digest(csrf_token, session_token))


@router.get("/login")
def login_form(request: Request):
    if current_user(request):
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    csrf_token = rotate_csrf_token(request)
    return templates.TemplateResponse(request, "login.html", {"csrf_token": csrf_token, "error": None})


@router.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...), csrf_token: str = Form(...)):
    if not is_valid_csrf_token(request, csrf_token):
        csrf_token = rotate_csrf_token(request)
        return templates.TemplateResponse(
            request,
            "login.html",
            {"csrf_token": csrf_token, "error": "Invalid login request."},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    request.session.pop("csrf_token", None)

    user = authenticate_user(username, password)
    if not user:
        csrf_token = rotate_csrf_token(request)
        return templates.TemplateResponse(
            request,
            "login.html",
            {"csrf_token": csrf_token, "error": "Invalid username or password."},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    request.session.clear()
    request.session["user_id"] = user["id"]
    rotate_csrf_token(request)
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/logout")
def logout(request: Request, csrf_token: str = Form(...)):
    if not current_user(request):
        return PlainTextResponse("Authentication required.", status_code=status.HTTP_401_UNAUTHORIZED)
    if not is_valid_csrf_token(request, csrf_token):
        return PlainTextResponse("Invalid logout request.", status_code=status.HTTP_400_BAD_REQUEST)
    request.session.clear()
    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/")
def home(request: Request):
    user = current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    regulations = list_regulations()
    csrf_token = request.session.get("csrf_token") or rotate_csrf_token(request)
    return templates.TemplateResponse(request, "index.html", {"regulations": regulations, "user": user, "csrf_token": csrf_token})
