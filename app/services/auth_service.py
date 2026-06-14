import secrets
import sqlite3

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError

from app.db.database import get_connection

_hasher = PasswordHasher()


def hash_password(password: str) -> str:
    return _hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return _hasher.verify(password_hash, password)
    except (VerifyMismatchError, VerificationError):
        return False


def create_user(username: str, password: str) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO users (username, password_hash)
            VALUES (?, ?)
            """,
            (username, hash_password(password)),
        )
        conn.commit()


def authenticate_user(username: str, password: str) -> dict | None:
    with get_connection() as conn:
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    if not user or not verify_password(password, user["password_hash"]):
        return None
    return {"id": user["id"], "username": user["username"]}


def get_user_by_id(user_id: int) -> dict | None:
    with get_connection() as conn:
        user = conn.execute("SELECT id, username FROM users WHERE id = ?", (user_id,)).fetchone()
    return dict(user) if user else None


def bootstrap_user(username: str, password: str) -> None:
    try:
        create_user(username, password)
    except sqlite3.IntegrityError:
        return


def generate_csrf_token() -> str:
    return secrets.token_urlsafe(32)
