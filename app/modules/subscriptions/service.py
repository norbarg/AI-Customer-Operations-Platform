from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.customers.repository import CustomerRepository
from app.modules.subscriptions.models import Subscription
from app.modules.subscriptions.repository import SubscriptionRepository
from app.modules.subscriptions.schemas import (
    SubscriptionCreate,
    SubscriptionUpdate,
)


class SubscriptionService:
    @staticmethod
    async def create_subscription(
        db: AsyncSession,
        data: SubscriptionCreate,
    ) -> Subscription:
        customer = await CustomerRepository.get_by_id(
            db,
            data.customer_id,
        )

        if customer is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found",
            )

        existing_subscription = await SubscriptionRepository.get_by_customer_id(
            db,
            data.customer_id,
        )

        if existing_subscription is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Customer already has a subscription",
            )

        return await SubscriptionRepository.create(db, data)

    @staticmethod
    async def get_subscription(
        db: AsyncSession,
        subscription_id: int,
    ) -> Subscription:
        subscription = await SubscriptionRepository.get_by_id(
            db,
            subscription_id,
        )

        if subscription is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subscription not found",
            )

        return subscription

    @staticmethod
    async def get_subscriptions(
        db: AsyncSession,
    ) -> list[Subscription]:
        return await SubscriptionRepository.get_all(db)

    @staticmethod
    async def update_subscription(
        db: AsyncSession,
        subscription_id: int,
        data: SubscriptionUpdate,
    ) -> Subscription:
        subscription = await SubscriptionService.get_subscription(
            db,
            subscription_id,
        )

        return await SubscriptionRepository.update(
            db,
            subscription,
            data,
        )

    @staticmethod
    async def delete_subscription(
        db: AsyncSession,
        subscription_id: int,
    ) -> None:
        subscription = await SubscriptionService.get_subscription(
            db,
            subscription_id,
        )

        await SubscriptionRepository.delete(
            db,
            subscription,
        )
