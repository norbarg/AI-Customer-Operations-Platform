from typing import Annotated

from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.customers.router import router as customers_router
from app.db.session import get_db

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

app.include_router(customers_router)


@app.get("/health")
async def health_check(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> dict[str, str]:
    await db.execute(text("SELECT 1"))

    return {
        "status": "ok",
        "database": "connected",
    }
