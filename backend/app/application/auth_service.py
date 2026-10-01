"""Deliberately simple auth: one user from env vars, opaque tokens kept in memory.

Trade-offs (fine for a demo, worth mentioning in an interview):
- tokens are lost when the backend restarts -> clients must log in again
- only works with a single uvicorn worker (tokens are per process)
"""

import os
import secrets

_tokens: set[str] = set()


def _expected_credentials() -> tuple[str, str]:
    return os.getenv("APP_USERNAME", "admin"), os.getenv("APP_PASSWORD", "admin123")


def login(username: str, password: str) -> str | None:
    expected_user, expected_password = _expected_credentials()
    user_ok = secrets.compare_digest(username, expected_user)
    password_ok = secrets.compare_digest(password, expected_password)
    if not (user_ok and password_ok):
        return None
    token = secrets.token_urlsafe(32)
    _tokens.add(token)
    return token


def is_valid(token: str) -> bool:
    return token in _tokens


def logout(token: str) -> None:
    _tokens.discard(token)
