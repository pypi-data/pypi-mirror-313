"""Renames existing block types and deletes removed block types

Revision ID: 628a873f0d1a
Revises: 061c7e518b40
Create Date: 2022-07-19 15:34:32.619181

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "628a873f0d1a"
down_revision = "56be24fdb383"
branch_labels = None
depends_on = None

BLOCK_TYPES_TO_RENAME = [
    {"OLD_NAME": "DateTime", "NEW_NAME": "Date Time"},
    {"OLD_NAME": "EnvironmentVariable", "NEW_NAME": "Environment Variable"},
    {"OLD_NAME": "KubernetesClusterConfig", "NEW_NAME": "Kubernetes Cluster Config"},
    {"OLD_NAME": "LocalFileSystem", "NEW_NAME": "Local File System"},
    {"OLD_NAME": "RemoteFileSystem", "NEW_NAME": "Remote File System"},
]

BLOCK_TYPES_TO_REMOVE = [
    "Azure Blob Storage",
    "File Storage",
    "Google Cloud Storage",
    "KV Server Storage",
    "Local Storage",
    "S3 Storage",
    "Temporary Local Storage",
]


def upgrade():
    connection = op.get_bind()
    meta_data = sa.MetaData()
    meta_data.reflect(connection)
    BLOCK_TYPE = meta_data.tables["block_type"]

    for block_type_rename_config in BLOCK_TYPES_TO_RENAME:
        connection.execute(
            sa.update(BLOCK_TYPE)
            .where(BLOCK_TYPE.c.name == block_type_rename_config["OLD_NAME"])
            .values(name=block_type_rename_config["NEW_NAME"])
        )
    for block_type_name in BLOCK_TYPES_TO_REMOVE:
        connection.execute(
            sa.delete(BLOCK_TYPE).where(BLOCK_TYPE.c.name == block_type_name)
        )


def downgrade():
    # Purely a data migration. No downgrade necessary.
    pass
