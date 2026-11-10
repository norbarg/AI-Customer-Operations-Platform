from datetime import datetime
from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class PaymentStatus(StrEnum):
    paid = "paid"
    failed = "failed"
    refunded = "refunded"


class PaymentCreate(BaseModel):
    subscription_id: int
    amount: Decimal = Field(gt=0)
    currency: str = Field(default="USD", min_length=3, max_length=3)
    external_id: str | None = None


class PaymentUpdate(BaseModel):
    status: PaymentStatus | None = None


class PaymentResponse(BaseModel):
    id: int
    subscription_id: int
    amount: Decimal
    currency: str
    status: PaymentStatus
    external_id: str | None
    paid_at: datetime

    model_config = ConfigDict(from_attributes=True)
