import asyncio
from uuid import uuid4

from app.db.session import get_session_factory
from app.workflow.repository import WorkflowRunRepository


async def _create_and_read_workflow_run() -> None:
    run_id = uuid4()
    async with get_session_factory()() as session:
        repository = WorkflowRunRepository(session)
        await repository.create(
            run_id=run_id,
            owner_id="demo-employee-001",
            workflow_id="document-assistant",
            workflow_version_id="document-assistant:demo",
            conversation_id=None,
            status="succeeded",
            inputs={"message": "测试"},
            answer="测试结果",
            citations=[],
        )

    async with get_session_factory()() as session:
        repository = WorkflowRunRepository(session)
        stored = await repository.get_visible(run_id, "demo-employee-001", False)

    assert stored is not None
    assert stored.answer == "测试结果"
    assert stored.inputs == {"message": "测试"}


def test_create_and_read_workflow_run() -> None:
    asyncio.run(_create_and_read_workflow_run())
