import sqlite3
from contextlib import contextmanager

from app.core.config import get_database_path


@contextmanager
def get_connection():
    conn = sqlite3.connect(get_database_path())
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()
