from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.customers.repository import CustomerRepository
from app.requests.models import Request
from app.requests.repository import RequestRepository
from app.requests.schemas import RequestCreate, RequestUpdate


class RequestService:
    @staticmethod
    async def create_request(
        db: AsyncSession,
        data: RequestCreate,
    ) -> Request:
        customer = await CustomerRepository.get_by_id(
            db,
            data.customer_id,
        )

        if customer is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found",
            )

        return await RequestRepository.create(
            db,
            data,
        )

    @staticmethod
    async def get_request(
        db: AsyncSession,
        request_id: int,
    ) -> Request:
        request = await RequestRepository.get_by_id(
            db,
            request_id,
        )

        if request is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Request not found",
            )

        return request

    @staticmethod
    async def get_requests(
        db: AsyncSession,
        customer_id: int | None = None,
    ) -> list[Request]:
        if customer_id is not None:
            return await RequestRepository.get_by_customer_id(
                db,
                customer_id,
            )

        return await RequestRepository.get_all(db)

    @staticmethod
    async def update_request(
        db: AsyncSession,
        request_id: int,
        data: RequestUpdate,
    ) -> Request:
        request = await RequestService.get_request(
            db,
            request_id,
        )

        return await RequestRepository.update(
            db,
            request,
            data,
        )

    @staticmethod
    async def delete_request(
        db: AsyncSession,
        request_id: int,
    ) -> None:
        request = await RequestService.get_request(
            db,
            request_id,
        )

        await RequestRepository.delete(
            db,
            request,
        )
