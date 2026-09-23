"""Permission boundary for workflow visibility and execution."""

from app.agent.catalog import AGENTS
from app.agent.schemas import AgentSummary


class PermissionService:
    """Calculate a user's effective Agent set.

    Returning a new list prevents route handlers from mutating the catalog.
    """

    _employee_workflows = {
        "document-assistant",
        "image-inspector",
        "tech-knowledge",
    }

    def get_effective_agents(self, user_id: str, role: str = "employee") -> list[AgentSummary]:
        del user_id
        allowed = {agent.id for agent in AGENTS} if role == "platform_admin" else self._employee_workflows
        return [agent for agent in AGENTS if agent.id in allowed]

    def can_execute_agent(self, user_id: str, agent_id: str, role: str = "employee") -> bool:
        return any(agent.id == agent_id for agent in self.get_effective_agents(user_id, role))
