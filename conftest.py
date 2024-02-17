"""This file is used to set the environment variable for testing."""

import os

os.environ["MODE"] = "testing"
os.environ["DSN"] = "sqlite+aiosqlite:///test_db.sqlite3"
