"""change user_qr_mpg.userid to TEXT

Revision ID: f2a3b4c5d6e7
Revises: e7f8g9h0i1j2
Create Date: 2025-08-26 00:48:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f2a3b4c5d6e7'
down_revision: Union[str, Sequence[str], None] = 'e7f8g9h0i1j2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()

    # Change type of user_qr_mpg.userid to TEXT if column exists
    exists = conn.execute(
        sa.text(
            """
            SELECT 1
            FROM information_schema.columns
            WHERE table_schema = current_schema()
              AND table_name = 'user_qr_mpg'
              AND column_name = 'userid'
            """
        )
    ).scalar()
    if exists:
        # Drop default if any
        conn.execute(sa.text('ALTER TABLE "user_qr_mpg" ALTER COLUMN userid DROP DEFAULT'))
        # Alter type using cast; handles integer -> text and is no-op for text
        conn.execute(sa.text('ALTER TABLE "user_qr_mpg" ALTER COLUMN userid TYPE TEXT USING userid::text'))


def downgrade() -> None:
    # Non-destructive downgrade omitted to preserve data
    pass


