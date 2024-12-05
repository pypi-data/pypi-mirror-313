"""Create `flow_run_input` table

Revision ID: 733ca1903976
Revises: 9c493c02ca6d
Create Date: 2023-12-07 09:53:20.009178

"""

import sqlalchemy as sa
from alembic import op

import prefect

# revision identifiers, used by Alembic.
revision = "733ca1903976"
down_revision = "9c493c02ca6d"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "flow_run_input",
        sa.Column(
            "id",
            prefect.server.utilities.database.UUID(),
            server_default=sa.text("(GEN_RANDOM_UUID())"),
            nullable=False,
        ),
        sa.Column(
            "created",
            prefect.server.utilities.database.Timestamp(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated",
            prefect.server.utilities.database.Timestamp(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("key", sa.String(), nullable=False),
        sa.Column("value", sa.Text(), nullable=False),
        sa.Column(
            "flow_run_id", prefect.server.utilities.database.UUID(), nullable=False
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_flow_run_input")),
        sa.UniqueConstraint(
            "flow_run_id", "key", name=op.f("uq_flow_run_input__flow_run_id_key")
        ),
    )
    op.create_index(
        op.f("ix_flow_run_input__updated"), "flow_run_input", ["updated"], unique=False
    )


def downgrade():
    op.drop_index(op.f("ix_flow_run_input__updated"), table_name="flow_run_input")
    op.drop_table("flow_run_input")
