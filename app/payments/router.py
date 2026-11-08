from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.payments.schemas import (
    PaymentCreate,
    PaymentResponse,
    PaymentUpdate,
)
from app.payments.service import PaymentService

router = APIRouter(
    prefix="/payments",
    tags=["Payments"],
)


@router.post(
    "",
    response_model=PaymentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_payment(
    data: PaymentCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> PaymentResponse:
    return await PaymentService.create_payment(db, data)


@router.get(
    "",
    response_model=list[PaymentResponse],
)
async def get_payments(
    db: Annotated[AsyncSession, Depends(get_db)],
    subscription_id: Annotated[int | None, Query()] = None,
) -> list[PaymentResponse]:
    return await PaymentService.get_payments(
        db,
        subscription_id,
    )


@router.get(
    "/{payment_id}",
    response_model=PaymentResponse,
)
async def get_payment(
    payment_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> PaymentResponse:
    return await PaymentService.get_payment(
        db,
        payment_id,
    )


@router.patch(
    "/{payment_id}",
    response_model=PaymentResponse,
)
async def update_payment(
    payment_id: int,
    data: PaymentUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> PaymentResponse:
    return await PaymentService.update_payment(
        db,
        payment_id,
        data,
    )
