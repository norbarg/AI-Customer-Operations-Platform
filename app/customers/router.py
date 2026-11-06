from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.customers.schemas import (
    CustomerCreate,
    CustomerResponse,
    CustomerUpdate,
)
from app.customers.service import CustomerService
from app.db.session import get_db

router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)


@router.post(
    "",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_customer(
    data: CustomerCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> CustomerResponse:
    return await CustomerService.create_customer(db, data)


@router.get(
    "",
    response_model=list[CustomerResponse],
)
async def get_customers(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[CustomerResponse]:
    return await CustomerService.get_customers(db)


@router.get(
    "/{customer_id}",
    response_model=CustomerResponse,
)
async def get_customer(
    customer_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> CustomerResponse:
    return await CustomerService.get_customer(db, customer_id)


@router.patch(
    "/{customer_id}",
    response_model=CustomerResponse,
)
async def update_customer(
    customer_id: int,
    data: CustomerUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> CustomerResponse:
    return await CustomerService.update_customer(
        db,
        customer_id,
        data,
    )


@router.delete(
    "/{customer_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_customer(
    customer_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> None:
    await CustomerService.delete_customer(
        db,
        customer_id,
    )
