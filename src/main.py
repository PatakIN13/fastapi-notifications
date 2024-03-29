"""
This is the main file of the project. It is responsible for creating the FastAPI app.
"""

from fastapi import FastAPI
from pydantic import BaseModel

from src.account.routers import router_account, router_role, router_admin_account

from src.core.settings import settings


app = FastAPI()
app.include_router(router_account, prefix=settings.main_url)
app.include_router(router_admin_account, prefix=settings.main_url)
app.include_router(router_role, prefix=settings.main_url)


class Status(BaseModel):
    """
    Status server response
    """

    status: str = "ok"


@app.get(settings.main_url + "/status", response_model=Status)
async def status():
    """
    Status endpoint
    """
    return Status()
