from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.customers.models import Customer
from app.customers.repository import CustomerRepository
from app.customers.schemas import CustomerCreate, CustomerUpdate


class CustomerService:
    @staticmethod
    async def create_customer(
        db: AsyncSession,
        data: CustomerCreate,
    ) -> Customer:
        existing_customer = await CustomerRepository.get_by_email(
            db,
            data.email,
        )

        if existing_customer is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Customer with this email already exists",
            )

        return await CustomerRepository.create(
            db,
            data,
        )

    @staticmethod
    async def get_customer(
        db: AsyncSession,
        customer_id: int,
    ) -> Customer:
        customer = await CustomerRepository.get_by_id(
            db,
            customer_id,
        )

        if customer is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found",
            )

        return customer

    @staticmethod
    async def get_customers(
        db: AsyncSession,
    ) -> list[Customer]:
        return await CustomerRepository.get_all(db)

    @staticmethod
    async def update_customer(
        db: AsyncSession,
        customer_id: int,
        data: CustomerUpdate,
    ) -> Customer:
        customer = await CustomerService.get_customer(
            db,
            customer_id,
        )

        if data.email is not None and data.email != customer.email:
            existing_customer = await CustomerRepository.get_by_email(
                db,
                data.email,
            )

            if existing_customer is not None:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Customer with this email already exists",
                )

        return await CustomerRepository.update(
            db,
            customer,
            data,
        )

    @staticmethod
    async def delete_customer(
        db: AsyncSession,
        customer_id: int,
    ) -> None:
        customer = await CustomerService.get_customer(
            db,
            customer_id,
        )

        await CustomerRepository.delete(
            db,
            customer,
        )
