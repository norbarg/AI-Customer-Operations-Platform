from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.customers.models import Customer
from app.customers.schemas import CustomerCreate, CustomerUpdate


class CustomerRepository:
    @staticmethod
    async def create(
        db: AsyncSession,
        data: CustomerCreate,
    ) -> Customer:
        customer = Customer(
            name=data.name,
            email=data.email,
            company_name=data.company_name,
            phone=data.phone,
        )

        db.add(customer)
        await db.commit()
        await db.refresh(customer)

        return customer

    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        customer_id: int,
    ) -> Customer | None:
        result = await db.execute(select(Customer).where(Customer.id == customer_id))

        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_email(
        db: AsyncSession,
        email: str,
    ) -> Customer | None:
        result = await db.execute(select(Customer).where(Customer.email == email))

        return result.scalar_one_or_none()

    @staticmethod
    async def get_all(
        db: AsyncSession,
    ) -> list[Customer]:
        result = await db.execute(select(Customer).order_by(Customer.id))

        return list(result.scalars().all())

    @staticmethod
    async def update(
        db: AsyncSession,
        customer: Customer,
        data: CustomerUpdate,
    ) -> Customer:
        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(customer, field, value)

        await db.commit()
        await db.refresh(customer)

        return customer

    @staticmethod
    async def delete(
        db: AsyncSession,
        customer: Customer,
    ) -> None:
        await db.delete(customer)
        await db.commit()
