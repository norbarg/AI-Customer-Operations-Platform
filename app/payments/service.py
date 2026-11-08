from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.payments.models import Payment
from app.payments.repository import PaymentRepository
from app.payments.schemas import PaymentCreate, PaymentUpdate
from app.subscriptions.repository import SubscriptionRepository


class PaymentService:
    @staticmethod
    async def create_payment(
        db: AsyncSession,
        data: PaymentCreate,
    ) -> Payment:
        subscription = await SubscriptionRepository.get_by_id(
            db,
            data.subscription_id,
        )

        if subscription is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subscription not found",
            )

        if data.external_id is not None:
            existing_payment = await PaymentRepository.get_by_external_id(
                db,
                data.external_id,
            )

            if existing_payment is not None:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Payment with this external ID already exists",
                )

        return await PaymentRepository.create(db, data)

    @staticmethod
    async def get_payment(
        db: AsyncSession,
        payment_id: int,
    ) -> Payment:
        payment = await PaymentRepository.get_by_id(
            db,
            payment_id,
        )

        if payment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payment not found",
            )

        return payment

    @staticmethod
    async def get_payments(
        db: AsyncSession,
        subscription_id: int | None = None,
    ) -> list[Payment]:
        if subscription_id is not None:
            return await PaymentRepository.get_by_subscription_id(
                db,
                subscription_id,
            )

        return await PaymentRepository.get_all(db)

    @staticmethod
    async def update_payment(
        db: AsyncSession,
        payment_id: int,
        data: PaymentUpdate,
    ) -> Payment:
        payment = await PaymentService.get_payment(
            db,
            payment_id,
        )

        return await PaymentRepository.update(
            db,
            payment,
            data,
        )
