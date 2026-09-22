"""Public DTOs for the Agent catalog."""

from typing import Literal

from pydantic import BaseModel


class AgentSummary(BaseModel):
    id: str
    name: str
    description: str
    category: str
    status: Literal["ready", "draft"]
    requires_knowledge_base: bool = False
