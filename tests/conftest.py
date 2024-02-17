"""Pytest configuration file for the tests directory."""

import asyncio
import json
from datetime import datetime

import pytest

from src.core.settings import settings
from src.core.database import db_helper, Base

from src.account.models import Account, Role


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    """Prepare the database for testing."""
    assert settings.mode == "testing"

    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json_file(model: str):
        with open(f"tests/data/mock_{model}.json", encoding="utf-8") as file:
            return json.load(file)

    role = open_mock_json_file("role")
    accounts = open_mock_json_file("account")

    for account in accounts:
        account["created_at"] = datetime.strptime(
            account["created_at"], "%Y-%m-%dT%H:%M:%S.%f"
        )

    async with db_helper.session_factory() as session:
        for role_data in role:
            role = Role(**role_data)
            session.add(role)
        for account_data in accounts:
            account = Account(**account_data)
            session.add(account)
        await session.commit()


@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
