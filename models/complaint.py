import sqlalchemy as sa

from db import metadata
from models.enums import State

Complaint = sa.Table(
    "complaints",
    metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('title', sa.String(120), unique=True),
    sa.Column("description", sa.String(255)),
    sa.Column("photo_url", sa.String(200)),
    sa.Column("amount", sa.Float, nullable=False),
    sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    sa.Column("status", sa.Enum(State), nullable=False, server_default=State.pending.name),
    sa.Column("complainer_id", sa.ForeignKey("users.id"), nullable=False)
)
