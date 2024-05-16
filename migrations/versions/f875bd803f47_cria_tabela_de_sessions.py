"""cria tabela de sessions

Revision ID: f875bd803f47
Revises: 08dcc1b8417b
Create Date: 2024-05-15 13:09:28.817887

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f875bd803f47"
down_revision: Union[str, None] = "08dcc1b8417b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "auth_sessions",
        sa.Column(
            "session_id", sa.String(length=32), nullable=False
        ),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("expire_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["auth_users.id"],
        ),
        sa.PrimaryKeyConstraint("session_id"),
    )
    op.create_index(op.f("ix_auth_sessions_user_id"), "auth_sessions", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_auth_sessions_user_id"), table_name="auth_sessions")
    op.drop_table("auth_sessions")
