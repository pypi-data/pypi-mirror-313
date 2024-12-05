"""Add BlockSchema capabilities

Revision ID: 33439667aeea
Revises: 888a0bb0df7b
Create Date: 2022-05-19 16:58:08.802305

"""

import sqlalchemy as sa
from alembic import op

import prefect

# revision identifiers, used by Alembic.
revision = "33439667aeea"
down_revision = "888a0bb0df7b"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("block_document", schema=None) as batch_op:
        batch_op.drop_constraint("fk_block__block_schema_id__block_schema")
    with op.batch_alter_table("block_schema", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "capabilities",
                prefect.server.utilities.database.JSON(astext_type=sa.Text()),
                server_default="[]",
                nullable=False,
            ),
        )

    connection = op.get_bind()
    meta_data = sa.MetaData()
    meta_data.reflect(connection)
    BLOCK_SCHEMA = meta_data.tables["block_schema"]

    results = connection.execute(sa.select(BLOCK_SCHEMA.c.id, BLOCK_SCHEMA.c.type))

    for id, type in results:
        if type == "STORAGE":
            connection.execute(
                sa.update(BLOCK_SCHEMA)
                .where(BLOCK_SCHEMA.c.id == id)
                .values(capabilities=["writeable", "readable", "storage"])
            )

    with op.batch_alter_table("block_schema", schema=None) as batch_op:
        batch_op.drop_index("ix_block_schema__type")
        batch_op.drop_column("type")

    with op.batch_alter_table(
        "block_document",
        schema=None,
    ) as batch_op:
        batch_op.create_foreign_key(
            batch_op.f("fk_block__block_schema_id__block_schema"),
            "block_schema",
            ["block_schema_id"],
            ["id"],
            ondelete="cascade",
        )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("block_schema", schema=None) as batch_op:
        batch_op.add_column(sa.Column("type", sa.VARCHAR(), nullable=True))
        batch_op.create_index("ix_block_schema__type", ["type"], unique=False)

    connection = op.get_bind()
    meta_data = sa.MetaData()
    meta_data.reflect(connection)
    BLOCK_SCHEMA = meta_data.tables["block_schema"]

    results = connection.execute(
        sa.select(BLOCK_SCHEMA.c.id, BLOCK_SCHEMA.c.capabilities)
    )

    for id, capabilities in results:
        if "storage" in capabilities:
            connection.execute(
                sa.update(BLOCK_SCHEMA)
                .where(BLOCK_SCHEMA.c.id == id)
                .values(type="STORAGE")
            )

    with op.batch_alter_table("block_schema", schema=None) as batch_op:
        batch_op.drop_column("capabilities")
    # ### end Alembic commands ###
