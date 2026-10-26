"""Explicit versioned migration; request handlers never create tables."""
from pathlib import Path

from alembic import command
from alembic.config import Config
from alembic.runtime.migration import MigrationContext
import sqlalchemy as sa

HEAD = "civicinspect_0001"


def source_engine(url):
    engine = sa.create_engine(url)
    if engine.dialect.name == "sqlite":
        @sa.event.listens_for(engine, "connect")
        def foreign_keys(connection, _record):
            connection.execute("PRAGMA foreign_keys=ON")
        return engine.execution_options(schema_translate_map={"civicinspect": None})
    if engine.dialect.name != "postgresql":
        engine.dispose()
        raise ValueError("Inspections requires PostgreSQL; SQLite is for affected repository checks only.")
    return engine


def upgrade(engine):
    config = Config()
    config.set_main_option("script_location", str(Path(__file__).parent))
    with engine.begin() as connection:
        if engine.dialect.name == "postgresql":
            connection.execute(sa.text("SELECT pg_advisory_xact_lock(80610001)"))
            connection.execute(sa.text("CREATE SCHEMA IF NOT EXISTS civicinspect"))
        config.attributes["connection"] = connection
        command.upgrade(config, "head")


def ready(engine):
    from civicinspect.workflow_schema import metadata
    schema = "civicinspect" if engine.dialect.name == "postgresql" else None
    with engine.connect() as connection:
        if not all(sa.inspect(connection).has_table(t.name, schema=schema) for t in metadata.tables.values()):
            return False
        return MigrationContext.configure(connection, opts={"version_table": "alembic_version_civicinspect",
            "version_table_schema": schema}).get_current_revision() == HEAD
