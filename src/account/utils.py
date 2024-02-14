"""This module contains utility functions for the account app."""

import bcrypt

from src.core.settings import settings


def generate_api_key(prefix_api_key: str = settings.prefix_api_key) -> str:
    """Generate an API key."""
    return f"{prefix_api_key}{bcrypt.gensalt().decode('utf-8')}"
