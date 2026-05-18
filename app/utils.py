"""
utils.py
--------
Utility helpers for the TaskManager application.
"""

import hashlib
import secrets


def hash_password(password: str) -> str:
    """Return a secure SHA-256 hash of the given password."""
    return hashlib.sha256(password.encode()).hexdigest()


def generate_token() -> str:
    """Generate a cryptographically secure random token."""
    return secrets.token_hex(32)


def paginate(items: list, page: int, per_page: int = 20) -> list:
    """Return a slice of items for the given page number."""
    start = (page - 1) * per_page
    return items[start: start + per_page]
