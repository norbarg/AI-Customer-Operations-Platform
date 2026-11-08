from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.requests.schemas import (
    RequestCreate,
    RequestResponse,
    RequestUpdate,
)
from app.requests.service import RequestService

router = APIRouter(
    prefix="/requests",
    tags=["Requests"],
)


@router.post(
    "",
    response_model=RequestResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_request(
    data: RequestCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> RequestResponse:
    return await RequestService.create_request(db, data)


@router.get(
    "",
    response_model=list[RequestResponse],
)
async def get_requests(
    db: Annotated[AsyncSession, Depends(get_db)],
    customer_id: Annotated[int | None, Query()] = None,
) -> list[RequestResponse]:
    return await RequestService.get_requests(
        db,
        customer_id,
    )


@router.get(
    "/{request_id}",
    response_model=RequestResponse,
)
async def get_request(
    request_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> RequestResponse:
    return await RequestService.get_request(
        db,
        request_id,
    )


@router.patch(
    "/{request_id}",
    response_model=RequestResponse,
)
async def update_request(
    request_id: int,
    data: RequestUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> RequestResponse:
    return await RequestService.update_request(
        db,
        request_id,
        data,
    )


@router.delete(
    "/{request_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_request(
    request_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> None:
    await RequestService.delete_request(
        db,
        request_id,
    )
