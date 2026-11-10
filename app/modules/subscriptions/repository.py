from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.subscriptions.models import Subscription
from app.modules.subscriptions.schemas import (
    SubscriptionCreate,
    SubscriptionUpdate,
)


class SubscriptionRepository:
    @staticmethod
    async def create(
        db: AsyncSession,
        data: SubscriptionCreate,
    ) -> Subscription:
        subscription = Subscription(
            customer_id=data.customer_id,
            plan=data.plan,
            seats=data.seats,
            ends_at=data.ends_at,
        )

        db.add(subscription)
        await db.commit()
        await db.refresh(subscription)

        return subscription

    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        subscription_id: int,
    ) -> Subscription | None:
        result = await db.execute(
            select(Subscription).where(Subscription.id == subscription_id)
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_customer_id(
        db: AsyncSession,
        customer_id: int,
    ) -> Subscription | None:
        result = await db.execute(
            select(Subscription).where(Subscription.customer_id == customer_id)
        )

        return result.scalar_one_or_none()

    @staticmethod
    async def get_all(
        db: AsyncSession,
    ) -> list[Subscription]:
        result = await db.execute(select(Subscription).order_by(Subscription.id))

        return list(result.scalars().all())

    @staticmethod
    async def update(
        db: AsyncSession,
        subscription: Subscription,
        data: SubscriptionUpdate,
    ) -> Subscription:
        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(subscription, field, value)

        await db.commit()
        await db.refresh(subscription)

        return subscription

    @staticmethod
    async def delete(
        db: AsyncSession,
        subscription: Subscription,
    ) -> None:
        await db.delete(subscription)
        await db.commit()
