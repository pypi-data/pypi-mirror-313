"""Add block_spec_id to blocks

Revision ID: c8ff35f94028
Revises: f327e877e423
Create Date: 2022-02-21 14:59:16.180033

"""

import sqlalchemy as sa
from alembic import op

import prefect

# revision identifiers, used by Alembic.
revision = "c8ff35f94028"
down_revision = "f327e877e423"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("block", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "block_spec_id",
                prefect.server.utilities.database.UUID(),
                nullable=False,
            )
        )
        batch_op.drop_constraint("uq_block__name", type_="unique")
        batch_op.create_index(
            "uq_block__spec_id_name", ["block_spec_id", "name"], unique=True
        )
        batch_op.create_foreign_key(
            batch_op.f("fk_block__block_spec_id__block_spec"),
            "block_spec",
            ["block_spec_id"],
            ["id"],
            ondelete="cascade",
        )
        batch_op.drop_column("blockref")
        batch_op.add_column(
            sa.Column(
                "is_default_storage_block",
                sa.Boolean(),
                server_default="0",
                nullable=True,
            )
        )
        batch_op.create_index(
            batch_op.f("ix_block__is_default_storage_block"),
            ["is_default_storage_block"],
            unique=False,
        )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("block", schema=None) as batch_op:
        batch_op.add_column(sa.Column("blockref", sa.VARCHAR(), nullable=True))
        batch_op.drop_constraint(
            batch_op.f("fk_block__block_spec_id__block_spec"), type_="foreignkey"
        )
        batch_op.drop_index("uq_block__spec_id_name")
        batch_op.create_unique_constraint("uq_block__name", ["name"])
        batch_op.drop_column("block_spec_id")
        batch_op.drop_index(batch_op.f("ix_block__is_default_storage_block"))
        batch_op.drop_column("is_default_storage_block")

    # ### end Alembic commands ###
