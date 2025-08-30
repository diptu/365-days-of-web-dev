"""0002_initial_tenant

Revision ID: b57790c87579
Revises: f422da8f92aa
Create Date: 2025-08-31 02:10:00.018302

"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b57790c87579"
down_revision = "f422da8f92aa"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Unqualified DDL; env.py sets search_path per tenant schema
    op.execute("""
        CREATE TABLE IF NOT EXISTS org_users (
            id uuid PRIMARY KEY,
            email varchar(320) NOT NULL UNIQUE,
            full_name varchar(200),
            created_at timestamptz NOT NULL DEFAULT now()
        );
    """)
    op.execute("""
        CREATE INDEX IF NOT EXISTS ix_org_users_email ON org_users (email);
    """)
    op.execute("""
        CREATE TABLE IF NOT EXISTS memberships (
            id uuid PRIMARY KEY,
            user_id uuid NOT NULL REFERENCES org_users(id) ON DELETE CASCADE,
            joined_at timestamptz NOT NULL DEFAULT now()
        );
    """)
    op.execute("""
        CREATE INDEX IF NOT EXISTS ix_memberships_user_id ON memberships (user_id);
    """)


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_memberships_user_id;")
    op.execute("DROP TABLE IF EXISTS memberships;")
    op.execute("DROP INDEX IF EXISTS ix_org_users_email;")
    op.execute("DROP TABLE IF EXISTS org_users;")
