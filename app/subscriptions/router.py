from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.subscriptions.schemas import (
    SubscriptionCreate,
    SubscriptionResponse,
    SubscriptionUpdate,
)
from app.subscriptions.service import SubscriptionService

router = APIRouter(
    prefix="/subscriptions",
    tags=["Subscriptions"],
)


@router.post(
    "",
    response_model=SubscriptionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_subscription(
    data: SubscriptionCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> SubscriptionResponse:
    return await SubscriptionService.create_subscription(db, data)


@router.get(
    "",
    response_model=list[SubscriptionResponse],
)
async def get_subscriptions(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[SubscriptionResponse]:
    return await SubscriptionService.get_subscriptions(db)


@router.get(
    "/{subscription_id}",
    response_model=SubscriptionResponse,
)
async def get_subscription(
    subscription_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> SubscriptionResponse:
    return await SubscriptionService.get_subscription(
        db,
        subscription_id,
    )


@router.patch(
    "/{subscription_id}",
    response_model=SubscriptionResponse,
)
async def update_subscription(
    subscription_id: int,
    data: SubscriptionUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> SubscriptionResponse:
    return await SubscriptionService.update_subscription(
        db,
        subscription_id,
        data,
    )


@router.delete(
    "/{subscription_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_subscription(
    subscription_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> None:
    await SubscriptionService.delete_subscription(
        db,
        subscription_id,
    )
