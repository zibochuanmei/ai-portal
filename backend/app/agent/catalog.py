"""Temporary in-memory Agent catalog used until PostgreSQL is connected."""

from app.agent.schemas import AgentSummary


AGENTS = [
    AgentSummary(
        id="document-assistant",
        name="文档整理助手",
        description="从 PDF、Word、TXT 中提取重点并生成结构化摘要。",
        category="通用办公",
        status="ready",
    ),
    AgentSummary(
        id="image-inspector",
        name="图片信息提取助手",
        description="识别图片中的文字、表格和关键业务信息。",
        category="多模态处理",
        status="ready",
    ),
    AgentSummary(
        id="tech-knowledge",
        name="技术知识库助手",
        description="基于技术部授权知识库回答内部研发问题。",
        category="部门知识库",
        status="ready",
        requires_knowledge_base=True,
    ),
    AgentSummary(
        id="finance-private",
        name="财务分析助手",
        description="仅面向财务部门处理受限财务资料。",
        category="部门知识库",
        status="ready",
        requires_knowledge_base=True,
    ),
]


def get_agent(agent_id: str) -> AgentSummary | None:
    return next((agent for agent in AGENTS if agent.id == agent_id), None)
