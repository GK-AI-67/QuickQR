"""add details_locked to lost_and_found_qr

Revision ID: n1o2p3q4r5s6
Revises: h1i2j3k4l5m6
Create Date: 2025-08-26 01:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'n1o2p3q4r5s6'
down_revision: Union[str, Sequence[str], None] = 'h1i2j3k4l5m6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    exists = conn.execute(
        sa.text(
            """
            SELECT 1 FROM information_schema.columns
            WHERE table_schema = current_schema()
              AND table_name = 'lost_and_found_qr'
              AND column_name = 'details_locked'
            """
        )
    ).scalar()
    if not exists:
        op.add_column('lost_and_found_qr', sa.Column('details_locked', sa.Boolean(), nullable=True, server_default=sa.text('false')))
        op.execute("ALTER TABLE lost_and_found_qr ALTER COLUMN details_locked DROP DEFAULT")


def downgrade() -> None:
    try:
        op.drop_column('lost_and_found_qr', 'details_locked')
    except Exception:
        pass


