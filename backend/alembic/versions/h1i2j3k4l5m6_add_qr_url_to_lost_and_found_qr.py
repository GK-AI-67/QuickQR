"""add qr_url to lost_and_found_qr

Revision ID: h1i2j3k4l5m6
Revises: g3h4i5j6k7l8
Create Date: 2025-08-26 01:15:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'h1i2j3k4l5m6'
down_revision: Union[str, Sequence[str], None] = 'g3h4i5j6k7l8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    exists = conn.execute(
        sa.text(
            """
            SELECT 1
            FROM information_schema.columns
            WHERE table_schema = current_schema()
              AND table_name = 'lost_and_found_qr'
              AND column_name = 'qr_url'
            """
        )
    ).scalar()
    if not exists:
        op.add_column('lost_and_found_qr', sa.Column('qr_url', sa.String(length=500), nullable=True))


def downgrade() -> None:
    try:
        op.drop_column('lost_and_found_qr', 'qr_url')
    except Exception:
        pass


