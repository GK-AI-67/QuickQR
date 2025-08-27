"""change user_dtls.userid to UUID

Revision ID: a1b2c3d4e5f6
Revises: e2abe79d1272
Create Date: 2025-08-26 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql as psql


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = 'e2abe79d1272'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Ensure extension available for gen_random_uuid(); alternatively use uuid-ossp uuid_generate_v4()
    op.execute('CREATE EXTENSION IF NOT EXISTS "pgcrypto"')

    # Drop any existing default/identity on the column so type change won't try to cast it
    op.execute('ALTER TABLE user_dtls ALTER COLUMN userid DROP DEFAULT')
    # For identity (if it was SERIAL/IDENTITY)
    op.execute('ALTER TABLE user_dtls ALTER COLUMN userid DROP IDENTITY IF EXISTS')

    # Convert existing INTEGER PKs to fresh UUID v4 values; sets column type to UUID
    op.alter_column(
        'user_dtls',
        'userid',
        existing_type=sa.Integer(),
        type_=psql.UUID(as_uuid=True),
        postgresql_using='gen_random_uuid()'
    )

    # Set DB-level default for future inserts
    op.execute('ALTER TABLE user_dtls ALTER COLUMN userid SET DEFAULT gen_random_uuid()')


def downgrade() -> None:
    """Downgrade schema."""
    # Drop default first
    op.execute('ALTER TABLE user_dtls ALTER COLUMN userid DROP DEFAULT')

    # Convert back to INTEGER (data will be reset to 0)
    op.alter_column(
        'user_dtls',
        'userid',
        existing_type=psql.UUID(as_uuid=True),
        type_=sa.Integer(),
        postgresql_using='0'
    )


