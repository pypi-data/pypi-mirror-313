"""Migrates block schemas with new secrets fields

Revision ID: e2dae764a603
Revises: 3bd87ecdac38
Create Date: 2022-07-06 14:28:24.493390

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "e2dae764a603"
down_revision = "3bd87ecdac38"
branch_labels = None
depends_on = None

BLOCKS_TO_MIGRATE = [
    {
        "BLOCK_TYPE_NAME": "S3 Storage",
        "OLD_CHECKSUM": (
            "sha256:3ffda32926202a34fc30d7618e4792f71088d37fbcf92c18d070104ca6da7431"
        ),
        "NEW_CHECKSUM": (
            "sha256:68ed6efe6ab724c5f36519803012af68a22965eccfa5944c94fa809b8b9a6e04"
        ),
        "CAPABILITIES": ["readable", "storage", "writeable"],
        "NEW_FIELDS": {
            "title": "S3StorageBlock",
            "description": "Store data in an AWS S3 bucket.",
            "type": "object",
            "properties": {
                "bucket": {"title": "Bucket", "type": "string"},
                "aws_access_key_id": {"title": "Aws Access Key Id", "type": "string"},
                "aws_secret_access_key": {
                    "title": "Aws Secret Access Key",
                    "type": "string",
                    "writeOnly": True,
                    "format": "password",
                },
                "aws_session_token": {"title": "Aws Session Token", "type": "string"},
                "profile_name": {"title": "Profile Name", "type": "string"},
                "region_name": {"title": "Region Name", "type": "string"},
            },
            "required": ["bucket"],
            "block_type_name": "S3 Storage",
            "secret_fields": ["aws_secret_access_key"],
            "block_schema_references": {},
        },
    },
    {
        "BLOCK_TYPE_NAME": "Azure Blob Storage",
        "OLD_CHECKSUM": (
            "sha256:4488e8f7d196f7627e3ead24ca136860f0a54d54f6c98533cf3ef2f4ba9cf51b"
        ),
        "NEW_CHECKSUM": (
            "sha256:2aef5e384a1f4a2d8dd0ff8c3b96d2c5eb5852462078b6915f7d756847341a42"
        ),
        "CAPABILITIES": ["readable", "storage", "writeable"],
        "NEW_FIELDS": {
            "title": "AzureBlobStorageBlock",
            "description": "Store data in an Azure blob storage container.",
            "type": "object",
            "properties": {
                "container": {"title": "Container", "type": "string"},
                "connection_string": {
                    "title": "Connection String",
                    "type": "string",
                    "writeOnly": True,
                    "format": "password",
                },
            },
            "required": ["container", "connection_string"],
            "block_type_name": "Azure Blob Storage",
            "secret_fields": ["connection_string"],
            "block_schema_references": {},
        },
    },
]


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    connection = op.get_bind()
    meta_data = sa.MetaData()
    meta_data.reflect(connection)
    BLOCK_TYPE = meta_data.tables["block_type"]
    BLOCK_SCHEMA = meta_data.tables["block_schema"]
    BLOCK_DOCUMENT = meta_data.tables["block_document"]

    for block_migration_config in BLOCKS_TO_MIGRATE:
        block_type_result = connection.execute(
            sa.select(BLOCK_TYPE.c.id).where(
                BLOCK_TYPE.c.name == block_migration_config["BLOCK_TYPE_NAME"]
            )
        ).first()
        old_block_schema_result = connection.execute(
            sa.select(BLOCK_SCHEMA.c.id).where(
                BLOCK_SCHEMA.c.checksum == block_migration_config["OLD_CHECKSUM"]
            )
        ).first()
        # Only run migration for this block if the type and old schema already exist
        if block_type_result is not None and old_block_schema_result is not None:
            # Check if new version of the schema is present
            new_block_schema_result = connection.execute(
                sa.select(BLOCK_SCHEMA.c.id).where(
                    BLOCK_SCHEMA.c.checksum == block_migration_config["NEW_CHECKSUM"]
                )
            ).first()
            if new_block_schema_result is None:
                # Create new schema if not present
                connection.execute(
                    sa.insert(BLOCK_SCHEMA).values(
                        checksum=block_migration_config["NEW_CHECKSUM"],
                        fields=block_migration_config["NEW_FIELDS"],
                        block_type_id=block_type_result[0],
                        capabilities=block_migration_config["CAPABILITIES"],
                    )
                )
                new_block_schema_result = connection.execute(
                    sa.select(BLOCK_SCHEMA.c.id).where(
                        BLOCK_SCHEMA.c.checksum
                        == block_migration_config["NEW_CHECKSUM"]
                    )
                ).first()
            # Get all block documents that use the old block schema
            existing_block_documents_result = connection.execute(
                sa.select(BLOCK_DOCUMENT.c.id).where(
                    BLOCK_DOCUMENT.c.block_schema_id == old_block_schema_result[0]
                )
            ).all()
            # Update all block documents using the old block schema to use new block schema
            for block_document in existing_block_documents_result:
                connection.execute(
                    sa.update(BLOCK_DOCUMENT)
                    .where(BLOCK_DOCUMENT.c.id == block_document[0])
                    .values(block_schema_id=new_block_schema_result[0])
                )
            # Remove the old unused block schema
            connection.execute(
                sa.delete(BLOCK_SCHEMA).where(
                    BLOCK_SCHEMA.c.id == old_block_schema_result[0]
                )
            )
    # ### end Alembic commands ###


def downgrade():
    # Purely a data migration for 2.0b8. No downgrade necessary.
    pass
