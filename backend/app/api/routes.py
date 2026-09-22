from datetime import datetime, timezone
from typing import Literal
from uuid import uuid4

from fastapi import APIRouter, File, UploadFile
from pydantic import BaseModel, Field

from app.agent.catalog import get_agent
from app.agent.schemas import AgentSummary
from app.core.logging import get_logger
from app.permission.service import PermissionService


router = APIRouter()
logger = get_logger(__name__)


class DemoUser(BaseModel):
    id: str
    display_name: str
    department: str
    role: Literal["employee", "platform_admin"]


class AgentRunRequest(BaseModel):
    agent_id: str
    message: str = Field(min_length=1, max_length=8000)
    file_ids: list[str] = Field(default_factory=list)


DEMO_USER = DemoUser(
    id="demo-employee-001",
    display_name="演示员工",
    department="技术部",
    role="employee",
)

permission_service = PermissionService()


@router.get("/me", response_model=DemoUser)
async def get_current_user() -> DemoUser:
    """演示身份接口，后续替换为企业 SSO/JWT 解析。"""
    return DEMO_USER


@router.get("/agents", response_model=list[AgentSummary])
async def list_visible_agents() -> list[AgentSummary]:
    """返回后端权限计算后的 Agent 列表。当前演示用户属于技术部。"""
    agents = permission_service.get_effective_agents(DEMO_USER.id)
    logger.info("agents_listed", user_id=DEMO_USER.id, count=len(agents))
    return agents


@router.post("/agent-runs")
async def create_agent_run(payload: AgentRunRequest) -> dict:
    agent = get_agent(payload.agent_id)
    if agent is None or not permission_service.can_execute_agent(DEMO_USER.id, payload.agent_id):
        logger.warning(
            "agent_run_rejected",
            user_id=DEMO_USER.id,
            agent_id=payload.agent_id,
            reason="agent_not_found",
        )
        return {"ok": False, "error": "agent_not_found"}

    logger.info(
        "agent_run_created",
        user_id=DEMO_USER.id,
        agent_id=agent.id,
        file_count=len(payload.file_ids),
    )
    return {
        "ok": True,
        "run_id": str(uuid4()),
        "agent_id": agent.id,
        "status": "completed",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "answer": f"这是 {agent.name} 的演示结果。已收到你的需求：{payload.message}",
        "citations": [],
    }


@router.post("/files")
async def upload_file(file: UploadFile = File(...)) -> dict:
    """文件上传占位接口，后续接入 MinIO、病毒扫描和异步解析。"""
    logger.info(
        "file_upload_received",
        user_id=DEMO_USER.id,
        filename=file.filename,
        content_type=file.content_type,
    )
    return {
        "file_id": str(uuid4()),
        "filename": file.filename,
        "content_type": file.content_type,
        "status": "uploaded_demo",
    }
