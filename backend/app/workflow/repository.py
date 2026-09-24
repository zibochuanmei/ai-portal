from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.workflow.models import WorkflowRun


class WorkflowRunRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self,
        *,
        run_id: UUID,
        owner_id: str,
        workflow_id: str,
        workflow_version_id: str,
        conversation_id: str | None,
        status: str,
        inputs: dict[str, Any],
        answer: str | None,
        citations: list[dict[str, Any]],
    ) -> WorkflowRun:
        run = WorkflowRun(
            run_id=run_id,
            owner_id=owner_id,
            workflow_id=workflow_id,
            workflow_version_id=workflow_version_id,
            conversation_id=conversation_id,
            status=status,
            inputs=inputs,
            answer=answer,
            citations=citations,
        )
        self.session.add(run)
        await self.session.commit()
        await self.session.refresh(run)
        return run

    async def get_visible(
        self,
        run_id: UUID,
        user_id: str,
        is_admin: bool,
    ) -> WorkflowRun | None:
        statement = select(WorkflowRun).where(WorkflowRun.run_id == run_id)
        if not is_admin:
            statement = statement.where(WorkflowRun.owner_id == user_id)
        return await self.session.scalar(statement)
