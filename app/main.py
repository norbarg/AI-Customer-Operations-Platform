from typing import Annotated

from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.router import router as ai_router
from app.core.config import settings
from app.db.session import get_db
from app.knowledge.documents.router import router as documents_router
from app.knowledge.search.router import router as search_router
from app.modules.approvals.router import router as approvals_router
from app.modules.customers.router import router as customers_router
from app.modules.payments.router import router as payments_router
from app.modules.requests.router import router as requests_router
from app.modules.subscriptions.router import router as subscriptions_router
from app.modules.tasks.router import router as tasks_router
from app.modules.users.router import router as users_router

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

app.include_router(customers_router)
app.include_router(requests_router)
app.include_router(users_router)
app.include_router(tasks_router)
app.include_router(approvals_router)
app.include_router(subscriptions_router)
app.include_router(payments_router)
app.include_router(documents_router)
app.include_router(search_router)
app.include_router(ai_router)


@app.get("/health")
async def health_check(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> dict[str, str]:
    await db.execute(text("SELECT 1"))

    return {
        "status": "ok",
        "database": "connected",
    }
