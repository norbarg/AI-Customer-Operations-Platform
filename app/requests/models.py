from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.approvals.models import Approval
    from app.tasks.models import Task


class Request(Base):
    __tablename__ = "requests"

    id: Mapped[int] = mapped_column(primary_key=True)

    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id", ondelete="CASCADE"),
        index=True,
    )

    type: Mapped[str] = mapped_column(
        String(30),
        default="other",
    )

    source: Mapped[str] = mapped_column(
        String(30),
        default="manual",
    )

    subject: Mapped[str] = mapped_column(
        String(255),
    )

    content: Mapped[str] = mapped_column(
        Text,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="open",
    )

    priority: Mapped[str] = mapped_column(
        String(30),
        default="normal",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    customer = relationship(
        "Customer",
        back_populates="requests",
    )

    tasks: Mapped[list["Task"]] = relationship(
        "Task",
        back_populates="request",
        cascade="all, delete-orphan",
    )

    approvals: Mapped[list["Approval"]] = relationship(
        "Approval",
        back_populates="request",
        cascade="all, delete-orphan",
    )
