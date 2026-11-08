from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.approvals.schemas import (
    ApprovalCreate,
    ApprovalResponse,
    ApprovalReview,
)
from app.approvals.service import ApprovalService
from app.db.session import get_db

router = APIRouter(
    prefix="/approvals",
    tags=["Approvals"],
)


@router.post(
    "",
    response_model=ApprovalResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_approval(
    data: ApprovalCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ApprovalResponse:
    return await ApprovalService.create_approval(db, data)


@router.get(
    "",
    response_model=list[ApprovalResponse],
)
async def get_approvals(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[ApprovalResponse]:
    return await ApprovalService.get_approvals(db)


@router.get(
    "/{approval_id}",
    response_model=ApprovalResponse,
)
async def get_approval(
    approval_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ApprovalResponse:
    return await ApprovalService.get_approval(db, approval_id)


@router.post(
    "/{approval_id}/approve",
    response_model=ApprovalResponse,
)
async def approve(
    approval_id: int,
    data: ApprovalReview,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ApprovalResponse:
    return await ApprovalService.review_approval(
        db,
        approval_id,
        data,
        "approved",
    )


@router.post(
    "/{approval_id}/reject",
    response_model=ApprovalResponse,
)
async def reject(
    approval_id: int,
    data: ApprovalReview,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ApprovalResponse:
    return await ApprovalService.review_approval(
        db,
        approval_id,
        data,
        "rejected",
    )
