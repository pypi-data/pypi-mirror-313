"""Remove flow runners

Revision ID: e085c9cbf8ce
Revises: bb4dc90d3e29
Create Date: 2022-07-21 13:31:34.045385

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "e085c9cbf8ce"
down_revision = "0cf7311d6ea6"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column("deployment", "flow_runner_type")
    op.drop_column("deployment", "flow_runner_config")
    op.drop_column("deployment", "description")
    op.drop_index(op.f("ix_flow_run__flow_runner_type"), table_name="flow_run")
    op.drop_column("flow_run", "flow_runner_type")
    op.drop_column("flow_run", "flow_runner_config")
    op.drop_column("flow_run", "empirical_config")


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "flow_run",
        sa.Column(
            "empirical_config",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'{}'::jsonb"),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.add_column(
        "flow_run",
        sa.Column(
            "flow_runner_config",
            postgresql.JSONB(astext_type=sa.Text()),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.add_column(
        "flow_run",
        sa.Column("flow_runner_type", sa.VARCHAR(), autoincrement=False, nullable=True),
    )

    op.create_index(
        op.f("ix_flow_run__flow_runner_type"),
        "flow_run",
        ["flow_runner_type"],
        unique=False,
    )

    op.add_column(
        "deployment",
        sa.Column("description", sa.TEXT(), autoincrement=False, nullable=True),
    )
    op.add_column(
        "deployment",
        sa.Column(
            "flow_runner_config",
            postgresql.JSONB(astext_type=sa.Text()),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.add_column(
        "deployment",
        sa.Column("flow_runner_type", sa.VARCHAR(), autoincrement=False, nullable=True),
    )
