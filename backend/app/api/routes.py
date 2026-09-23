from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Literal
from uuid import uuid4

from fastapi import APIRouter, Depends, File, UploadFile, status
from pydantic import BaseModel, Field

from app.agent.catalog import get_agent
from app.agent.schemas import AgentSummary, WorkflowSummary
from app.auth.service import UserContext, get_current_user, require_platform_admin
from app.core.errors import ApiError
from app.core.logging import get_logger
from app.file.service import file_service
from app.permission.service import PermissionService


router = APIRouter()
logger = get_logger(__name__)
permission_service = PermissionService()


class WorkflowRunRequest(BaseModel):
    conversation_id: str | None = None
    file_ids: list[str] = Field(default_factory=list)
    inputs: dict[str, Any] = Field(default_factory=dict)


class WorkflowRunResponse(BaseModel):
    run_id: str
    task_id: str
    workflow_id: str
    workflow_version_id: str
    conversation_id: str | None
    status: Literal["queued", "running", "succeeded", "failed", "cancelled"]
    created_at: str
    answer: str | None = None
    citations: list[dict[str, Any]] = Field(default_factory=list)


@dataclass(frozen=True)
class StoredWorkflowRun:
    owner_id: str
    response: WorkflowRunResponse


_runs: dict[str, StoredWorkflowRun] = {}


def _workflow_summary(agent: AgentSummary) -> WorkflowSummary:
    return WorkflowSummary(
        workflow_id=agent.id,
        name=agent.name,
        description=agent.description,
        category=agent.category,
        status=agent.status,
        requires_knowledge_base=agent.requires_knowledge_base,
        can_run=True,
    )


def _require_workflow(user: UserContext, workflow_id: str) -> AgentSummary:
    workflow = get_agent(workflow_id)
    if workflow is None or not permission_service.can_execute_agent(user.id, workflow_id, user.role):
        raise ApiError(404, "WORKFLOW_NOT_FOUND", "工作流不存在或当前身份无权使用")
    return workflow


@router.get("/me", response_model=UserContext)
async def get_current_user_info(user: UserContext = Depends(get_current_user)) -> UserContext:
    return user


@router.get("/workflows", response_model=list[WorkflowSummary])
async def list_workflows(user: UserContext = Depends(get_current_user)) -> list[WorkflowSummary]:
    workflows = permission_service.get_effective_agents(user.id, user.role)
    logger.info("workflows_listed", user_id=user.id, count=len(workflows))
    return [_workflow_summary(item) for item in workflows]


@router.get("/workflows/{workflow_id}", response_model=WorkflowSummary)
async def get_workflow_detail(
    workflow_id: str,
    user: UserContext = Depends(get_current_user),
) -> WorkflowSummary:
    return _workflow_summary(_require_workflow(user, workflow_id))


@router.post(
    "/workflows/{workflow_id}/runs",
    response_model=WorkflowRunResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def create_workflow_run(
    workflow_id: str,
    payload: WorkflowRunRequest,
    user: UserContext = Depends(get_current_user),
) -> WorkflowRunResponse:
    workflow = _require_workflow(user, workflow_id)
    for file_id in payload.file_ids:
        file_service.require_owned(user, file_id)

    run_id = str(uuid4())
    message = str(payload.inputs.get("message", ""))
    run = WorkflowRunResponse(
        run_id=run_id,
        task_id=run_id,
        workflow_id=workflow.id,
        workflow_version_id=f"{workflow.id}:demo",
        conversation_id=payload.conversation_id,
        status="succeeded",
        created_at=datetime.now(timezone.utc).isoformat(),
        answer=f"这是 {workflow.name} 的演示结果。已收到你的需求：{message}",
        citations=[],
    )
    _runs[run_id] = StoredWorkflowRun(owner_id=user.id, response=run)
    logger.info("workflow_run_created", user_id=user.id, workflow_id=workflow.id, run_id=run_id)
    return run


@router.get("/workflow-runs/{run_id}", response_model=WorkflowRunResponse)
async def get_workflow_run(run_id: str, user: UserContext = Depends(get_current_user)) -> WorkflowRunResponse:
    stored = _runs.get(run_id)
    if stored is None or (stored.owner_id != user.id and user.role != "platform_admin"):
        raise ApiError(404, "RUN_NOT_FOUND", "运行记录不存在")
    return stored.response


@router.get("/workflow-runs/{run_id}/result", response_model=WorkflowRunResponse)
async def get_workflow_result(run_id: str, user: UserContext = Depends(get_current_user)) -> WorkflowRunResponse:
    return await get_workflow_run(run_id, user)


@router.post("/files", status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...),
    user: UserContext = Depends(get_current_user),
) -> dict[str, Any]:
    stored = await file_service.store(user, file)
    logger.info("file_uploaded", user_id=user.id, file_id=stored.file_id, size=stored.size)
    return {
        "file_id": stored.file_id,
        "filename": stored.filename,
        "content_type": stored.content_type,
        "size": stored.size,
        "status": "uploaded",
    }


@router.get("/admin/overview")
async def admin_overview(user: UserContext = Depends(get_current_user)) -> dict[str, Any]:
    require_platform_admin(user)
    return {"users": 0, "workflows": len(permission_service.get_effective_agents(user.id, user.role))}


# Compatibility alias for the first unshared skeleton. New code must use /workflows.
@router.get("/agents", response_model=list[AgentSummary], include_in_schema=False)
async def list_agents_legacy(user: UserContext = Depends(get_current_user)) -> list[AgentSummary]:
    return permission_service.get_effective_agents(user.id, user.role)
