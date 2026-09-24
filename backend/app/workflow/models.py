from datetime import datetime
from typing import Any
from uuid import UUID

from sqlalchemy import DateTime, Index, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID as PostgreSQLUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class WorkflowRun(Base):
    __tablename__ = "workflow_runs"
    __table_args__ = (
        Index("ix_workflow_runs_owner_created", "owner_id", "created_at"),
        Index("ix_workflow_runs_conversation_created", "conversation_id", "created_at"),
        Index("ix_workflow_runs_workflow_created", "workflow_id", "created_at"),
    )

    run_id: Mapped[UUID] = mapped_column(PostgreSQLUUID(as_uuid=True), primary_key=True)
    owner_id: Mapped[str] = mapped_column(String(128), nullable=False)
    workflow_id: Mapped[str] = mapped_column(String(128), nullable=False)
    workflow_version_id: Mapped[str] = mapped_column(String(160), nullable=False)
    conversation_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    inputs: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    answer: Mapped[str | None] = mapped_column(Text, nullable=True)
    citations: Mapped[list[dict[str, Any]]] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
