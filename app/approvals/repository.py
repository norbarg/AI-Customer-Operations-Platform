from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.approvals.models import Approval
from app.approvals.schemas import ApprovalCreate


class ApprovalRepository:
    @staticmethod
    async def create(
        db: AsyncSession,
        data: ApprovalCreate,
    ) -> Approval:
        approval = Approval(
            request_id=data.request_id,
            action_type=data.action_type,
            payload=data.payload,
        )

        db.add(approval)
        await db.commit()
        await db.refresh(approval)

        return approval

    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        approval_id: int,
    ) -> Approval | None:
        result = await db.execute(select(Approval).where(Approval.id == approval_id))

        return result.scalar_one_or_none()

    @staticmethod
    async def get_all(
        db: AsyncSession,
    ) -> list[Approval]:
        result = await db.execute(select(Approval).order_by(Approval.id))

        return list(result.scalars().all())

    @staticmethod
    async def review(
        db: AsyncSession,
        approval: Approval,
        status: str,
        reviewed_by: int,
        comment: str | None,
    ) -> Approval:
        approval.status = status
        approval.reviewed_by = reviewed_by
        approval.review_comment = comment
        approval.reviewed_at = datetime.now(UTC)

        await db.commit()
        await db.refresh(approval)

        return approval
