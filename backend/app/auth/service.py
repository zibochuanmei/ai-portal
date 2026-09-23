from typing import Literal

from fastapi import Request
from pydantic import BaseModel

from app.core.config import get_settings
from app.core.errors import ApiError


class UserContext(BaseModel):
    id: str
    display_name: str
    department: str
    role: Literal["employee", "platform_admin"]


DEMO_USERS: dict[str, UserContext] = {
    "demo-employee-001": UserContext(
        id="demo-employee-001",
        display_name="演示员工",
        department="技术部",
        role="employee",
    ),
    "demo-employee-002": UserContext(
        id="demo-employee-002",
        display_name="演示员工二号",
        department="生产部",
        role="employee",
    ),
    "demo-admin-001": UserContext(
        id="demo-admin-001",
        display_name="平台管理员",
        department="信息技术部",
        role="platform_admin",
    ),
}


def get_current_user(request: Request) -> UserContext:
    """Resolve demo identity now and leave one seam for OIDC/JWT later."""

    settings = get_settings()
    if settings.auth_mode != "demo":
        raise ApiError(501, "AUTH_NOT_CONFIGURED", "企业身份认证尚未配置")

    user_id = request.headers.get("X-Demo-User", "demo-employee-001")
    user = DEMO_USERS.get(user_id)
    if user is None:
        raise ApiError(401, "INVALID_DEMO_USER", "演示身份无效")
    return user


def require_platform_admin(user: UserContext) -> UserContext:
    if user.role != "platform_admin":
        raise ApiError(403, "ADMIN_REQUIRED", "需要平台管理员权限")
    return user
