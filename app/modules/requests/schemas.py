from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict


class RequestType(StrEnum):
    sales = "sales"
    support = "support"
    billing = "billing"
    refund = "refund"
    other = "other"


class RequestSource(StrEnum):
    email = "email"
    web = "web"
    manual = "manual"
    api = "api"


class RequestStatus(StrEnum):
    open = "open"
    in_progress = "in_progress"
    resolved = "resolved"
    closed = "closed"


class RequestPriority(StrEnum):
    low = "low"
    normal = "normal"
    high = "high"
    urgent = "urgent"


class RequestCreate(BaseModel):
    customer_id: int
    type: RequestType = RequestType.other
    source: RequestSource = RequestSource.manual
    subject: str
    content: str
    priority: RequestPriority = RequestPriority.normal


class RequestUpdate(BaseModel):
    type: RequestType | None = None
    source: RequestSource | None = None
    subject: str | None = None
    content: str | None = None
    status: RequestStatus | None = None
    priority: RequestPriority | None = None


class RequestResponse(BaseModel):
    id: int
    customer_id: int
    type: RequestType
    source: RequestSource
    subject: str
    content: str
    status: RequestStatus
    priority: RequestPriority
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
