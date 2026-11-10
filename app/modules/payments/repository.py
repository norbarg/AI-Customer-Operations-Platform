from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.payments.models import Payment
from app.modules.payments.schemas import PaymentCreate, PaymentUpdate


class PaymentRepository:
    @staticmethod
    async def create(
        db: AsyncSession,
        data: PaymentCreate,
    ) -> Payment:
        payment = Payment(
            subscription_id=data.subscription_id,
            amount=data.amount,
            currency=data.currency.upper(),
            external_id=data.external_id,
        )

        db.add(payment)
        await db.commit()
        await db.refresh(payment)

        return payment

    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        payment_id: int,
    ) -> Payment | None:
        result = await db.execute(select(Payment).where(Payment.id == payment_id))

        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_external_id(
        db: AsyncSession,
        external_id: str,
    ) -> Payment | None:
        result = await db.execute(
            select(Payment).where(Payment.external_id == external_id)
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def get_all(
        db: AsyncSession,
    ) -> list[Payment]:
        result = await db.execute(select(Payment).order_by(Payment.id))

        return list(result.scalars().all())

    @staticmethod
    async def get_by_subscription_id(
        db: AsyncSession,
        subscription_id: int,
    ) -> list[Payment]:
        result = await db.execute(
            select(Payment)
            .where(Payment.subscription_id == subscription_id)
            .order_by(Payment.id)
        )

        return list(result.scalars().all())

    @staticmethod
    async def update(
        db: AsyncSession,
        payment: Payment,
        data: PaymentUpdate,
    ) -> Payment:
        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(payment, field, value)

        await db.commit()
        await db.refresh(payment)

        return payment
