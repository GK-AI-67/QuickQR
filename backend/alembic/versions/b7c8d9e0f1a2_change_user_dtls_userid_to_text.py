"""change user_dtls.userid to TEXT

Revision ID: b7c8d9e0f1a2
Revises: a1b2c3d4e5f6
Create Date: 2025-08-26 00:05:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql as psql


# revision identifiers, used by Alembic.
revision: str = 'b7c8d9e0f1a2'
down_revision: Union[str, Sequence[str], None] = 'a1b2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Remove default if any set on UUID
    op.execute('ALTER TABLE user_dtls ALTER COLUMN userid DROP DEFAULT')

    # Convert UUID to TEXT
    op.alter_column(
        'user_dtls',
        'userid',
        existing_type=psql.UUID(as_uuid=True),
        type_=sa.Text(),
        postgresql_using='userid::text'
    )

    # Optional: set no default at DB level, app supplies string uuid


def downgrade() -> None:
    """Downgrade schema."""
    # Convert TEXT back to UUID (will fail if any non-uuid strings exist)
    op.alter_column(
        'user_dtls',
        'userid',
        existing_type=sa.Text(),
        type_=psql.UUID(as_uuid=True),
        postgresql_using='userid::uuid'
    )
    # Optionally re-add default
    op.execute('CREATE EXTENSION IF NOT EXISTS "pgcrypto"')
    op.execute('ALTER TABLE user_dtls ALTER COLUMN userid SET DEFAULT gen_random_uuid()')


