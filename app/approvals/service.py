from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.approvals.models import Approval
from app.approvals.repository import ApprovalRepository
from app.approvals.schemas import ApprovalCreate, ApprovalReview
from app.requests.repository import RequestRepository
from app.users.repository import UserRepository


class ApprovalService:
    @staticmethod
    async def create_approval(
        db: AsyncSession,
        data: ApprovalCreate,
    ) -> Approval:
        request = await RequestRepository.get_by_id(
            db,
            data.request_id,
        )

        if request is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Request not found",
            )

        return await ApprovalRepository.create(db, data)

    @staticmethod
    async def get_approval(
        db: AsyncSession,
        approval_id: int,
    ) -> Approval:
        approval = await ApprovalRepository.get_by_id(
            db,
            approval_id,
        )

        if approval is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Approval not found",
            )

        return approval

    @staticmethod
    async def get_approvals(
        db: AsyncSession,
    ) -> list[Approval]:
        return await ApprovalRepository.get_all(db)

    @staticmethod
    async def review_approval(
        db: AsyncSession,
        approval_id: int,
        data: ApprovalReview,
        new_status: str,
    ) -> Approval:
        approval = await ApprovalService.get_approval(
            db,
            approval_id,
        )

        if approval.status != "pending":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Approval has already been reviewed",
            )

        reviewer = await UserRepository.get_by_id(
            db,
            data.reviewed_by,
        )

        if reviewer is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reviewer not found",
            )

        return await ApprovalRepository.review(
            db,
            approval,
            new_status,
            data.reviewed_by,
            data.comment,
        )
