from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class SubscriptionPlan(StrEnum):
    starter = "starter"
    pro = "pro"
    enterprise = "enterprise"


class SubscriptionStatus(StrEnum):
    active = "active"
    cancelled = "cancelled"
    expired = "expired"


class SubscriptionCreate(BaseModel):
    customer_id: int
    plan: SubscriptionPlan
    seats: int = Field(default=1, ge=1)
    ends_at: datetime | None = None


class SubscriptionUpdate(BaseModel):
    plan: SubscriptionPlan | None = None
    seats: int | None = Field(default=None, ge=1)
    status: SubscriptionStatus | None = None
    ends_at: datetime | None = None


class SubscriptionResponse(BaseModel):
    id: int
    customer_id: int
    plan: SubscriptionPlan
    seats: int
    status: SubscriptionStatus
    started_at: datetime
    ends_at: datetime | None

    model_config = ConfigDict(from_attributes=True)
