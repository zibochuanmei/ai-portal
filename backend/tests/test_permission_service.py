from app.permission.service import PermissionService


def test_effective_agents_excludes_disabled_agent() -> None:
    service = PermissionService()

    visible_agents = service.get_effective_agents("demo-employee-001")

    assert [agent.id for agent in visible_agents] == [
        "document-assistant",
        "image-inspector",
        "tech-knowledge",
    ]
