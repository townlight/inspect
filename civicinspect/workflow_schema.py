"""Additive schema; old sample intake tables are retained unchanged."""
import sqlalchemy as sa

metadata = sa.MetaData(schema="civicinspect")

heads = sa.Table("connected_heads", metadata,
    sa.Column("entity_id", sa.String(160), primary_key=True),
    sa.Column("kind", sa.String(20), nullable=False),
    sa.Column("revision_id", sa.String(36), nullable=False))
revisions = sa.Table("connected_revisions", metadata,
    sa.Column("revision_id", sa.String(36), primary_key=True),
    sa.Column("entity_id", sa.String(160), sa.ForeignKey(heads.c.entity_id), nullable=False),
    sa.Column("parent_revision", sa.String(36)),
    sa.Column("payload", sa.JSON, nullable=False),
    sa.Column("sha256", sa.String(64), nullable=False),
    sa.Column("actor_id", sa.String(255), nullable=False),
    sa.Column("created_at", sa.String(40), nullable=False))
packets = sa.Table("connected_packets", metadata,
    sa.Column("packet_id", sa.String(36), primary_key=True),
    sa.Column("case_id", sa.String(160), sa.ForeignKey(heads.c.entity_id), nullable=False),
    sa.Column("revision_id", sa.String(36), sa.ForeignKey(revisions.c.revision_id), nullable=False),
    sa.Column("visibility", sa.String(20), nullable=False),
    sa.Column("text", sa.Text, nullable=False),
    sa.Column("sha256", sa.String(64), nullable=False),
    sa.Column("actor_id", sa.String(255), nullable=False),
    sa.Column("created_at", sa.String(40), nullable=False),
    sa.CheckConstraint("visibility IN ('staff_only', 'records_copy')"))
events = sa.Table("connected_events", metadata,
    sa.Column("event_id", sa.String(36), primary_key=True),
    sa.Column("entity_id", sa.String(160), sa.ForeignKey(heads.c.entity_id), nullable=False),
    sa.Column("sequence", sa.Integer, nullable=False),
    sa.Column("timestamp", sa.String(40), nullable=False),
    sa.Column("actor_id", sa.String(255), nullable=False),
    sa.Column("action", sa.String(100), nullable=False),
    sa.Column("details", sa.JSON, nullable=False),
    sa.Column("previous_hash", sa.String(64), nullable=False),
    sa.Column("entry_hash", sa.String(64), nullable=False),
    sa.UniqueConstraint("entity_id", "sequence"))
IMMUTABLE_TABLES = (revisions, packets, events)
