from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.requests.models import Request
from app.requests.schemas import RequestCreate, RequestUpdate


class RequestRepository:
    @staticmethod
    async def create(
        db: AsyncSession,
        data: RequestCreate,
    ) -> Request:
        request = Request(
            customer_id=data.customer_id,
            type=data.type,
            source=data.source,
            subject=data.subject,
            content=data.content,
            priority=data.priority,
        )

        db.add(request)
        await db.commit()
        await db.refresh(request)

        return request

    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        request_id: int,
    ) -> Request | None:
        result = await db.execute(select(Request).where(Request.id == request_id))

        return result.scalar_one_or_none()

    @staticmethod
    async def get_all(
        db: AsyncSession,
    ) -> list[Request]:
        result = await db.execute(select(Request).order_by(Request.id))

        return list(result.scalars().all())

    @staticmethod
    async def get_by_customer_id(
        db: AsyncSession,
        customer_id: int,
    ) -> list[Request]:
        result = await db.execute(
            select(Request)
            .where(Request.customer_id == customer_id)
            .order_by(Request.id)
        )

        return list(result.scalars().all())

    @staticmethod
    async def update(
        db: AsyncSession,
        request: Request,
        data: RequestUpdate,
    ) -> Request:
        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(request, field, value)

        await db.commit()
        await db.refresh(request)

        return request

    @staticmethod
    async def delete(
        db: AsyncSession,
        request: Request,
    ) -> None:
        await db.delete(request)
        await db.commit()
