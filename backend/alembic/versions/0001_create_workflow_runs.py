"""create workflow runs

Revision ID: 0001_create_workflow_runs
Revises:
Create Date: 2026-09-24
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "0001_create_workflow_runs"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "workflow_runs",
        sa.Column("run_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("owner_id", sa.String(length=128), nullable=False),
        sa.Column("workflow_id", sa.String(length=128), nullable=False),
        sa.Column("workflow_version_id", sa.String(length=160), nullable=False),
        sa.Column("conversation_id", sa.String(length=128), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("inputs", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("answer", sa.Text(), nullable=True),
        sa.Column("citations", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.PrimaryKeyConstraint("run_id"),
    )
    op.create_index("ix_workflow_runs_owner_created", "workflow_runs", ["owner_id", "created_at"])
    op.create_index("ix_workflow_runs_conversation_created", "workflow_runs", ["conversation_id", "created_at"])
    op.create_index("ix_workflow_runs_workflow_created", "workflow_runs", ["workflow_id", "created_at"])


def downgrade() -> None:
    op.drop_index("ix_workflow_runs_workflow_created", table_name="workflow_runs")
    op.drop_index("ix_workflow_runs_conversation_created", table_name="workflow_runs")
    op.drop_index("ix_workflow_runs_owner_created", table_name="workflow_runs")
    op.drop_table("workflow_runs")
