from alembic import context
from civicinspect.workflow_schema import metadata

connection = context.config.attributes["connection"]
context.configure(connection=connection, target_metadata=metadata,
    version_table="alembic_version_civicinspect",
    version_table_schema="civicinspect" if connection.dialect.name == "postgresql" else None)
with context.begin_transaction():
    context.run_migrations()
