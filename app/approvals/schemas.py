from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict


class ApprovalStatus(StrEnum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class ApprovalCreate(BaseModel):
    request_id: int
    action_type: str
    payload: dict[str, Any]


class ApprovalReview(BaseModel):
    reviewed_by: int
    comment: str | None = None


class ApprovalResponse(BaseModel):
    id: int
    request_id: int
    action_type: str
    payload: dict[str, Any]
    status: ApprovalStatus
    reviewed_by: int | None
    review_comment: str | None
    created_at: datetime
    reviewed_at: datetime | None

    model_config = ConfigDict(from_attributes=True)
