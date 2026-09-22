"""Permission boundary for Agent visibility and execution.

The first implementation is deliberately in-memory. The public methods are
the seam that will later query ``agent_grants`` and apply deny precedence.
"""

from app.agent.catalog import AGENTS
from app.agent.schemas import AgentSummary


class PermissionService:
    """Calculate a user's effective Agent set.

    Returning a new list prevents route handlers from mutating the catalog.
    """

    def get_effective_agents(self, user_id: str) -> list[AgentSummary]:
        del user_id  # The demo catalog is the same for the simulated user.
        return list(AGENTS)

    def can_execute_agent(self, user_id: str, agent_id: str) -> bool:
        return any(agent.id == agent_id for agent in self.get_effective_agents(user_id))

