from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class CustomerCreate(BaseModel):
    name: str
    email: EmailStr
    company_name: str | None = None
    phone: str | None = None


class CustomerUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    company_name: str | None = None
    phone: str | None = None
    status: str | None = None


class CustomerResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    company_name: str | None
    phone: str | None
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
