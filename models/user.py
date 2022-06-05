import sqlalchemy as sa

from db import metadata
from models.enums import RollType

User = sa.Table(
    "users",
    metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('email', sa.String(120), unique=True),
    sa.Column("password", sa.String(255)),
    sa.Column("first_name", sa.String(200)),
    sa.Column("last_name", sa.String(200)),
    sa.Column("phone", sa.String(13)),
    sa.Column("role", sa.Enum(RollType), nullable=False, server_default=RollType.complainer.name),
    sa.Column("iban", sa.String(200))
)
