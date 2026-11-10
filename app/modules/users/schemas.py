from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, EmailStr


class UserRole(StrEnum):
    admin = "admin"
    manager = "manager"
    agent = "agent"


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    role: UserRole = UserRole.agent


class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    role: UserRole | None = None
    is_active: bool | None = None


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: UserRole
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
