"""add missing columns to user_qr_mpg

Revision ID: e7f8g9h0i1j2
Revises: d1e2f3g4h5i6
Create Date: 2025-08-26 00:42:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e7f8g9h0i1j2'
down_revision: Union[str, Sequence[str], None] = 'd1e2f3g4h5i6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()

    def add_column_if_missing(table: str, column_def: str, col_name: str) -> None:
        exists = conn.execute(
            sa.text(
                """
                SELECT 1
                FROM information_schema.columns
                WHERE table_schema = current_schema()
                  AND table_name = :t
                  AND column_name = :c
                """
            ),
            {"t": table, "c": col_name},
        ).scalar()
        if not exists:
            conn.execute(sa.text(f'ALTER TABLE "{table}" ADD COLUMN {column_def}'))

    # Add missing columns used by the application
    add_column_if_missing('user_qr_mpg', 'scan_location VARCHAR(255)', 'scan_location')
    add_column_if_missing('user_qr_mpg', 'scan_ip VARCHAR(45)', 'scan_ip')
    add_column_if_missing('user_qr_mpg', 'scan_user_agent TEXT', 'scan_user_agent')
    add_column_if_missing('user_qr_mpg', 'scan_date TIMESTAMP', 'scan_date')
    add_column_if_missing('user_qr_mpg', 'is_first_scan BOOLEAN DEFAULT TRUE', 'is_first_scan')
    add_column_if_missing('user_qr_mpg', 'details_updated BOOLEAN DEFAULT FALSE', 'details_updated')
    add_column_if_missing('user_qr_mpg', 'created_date TIMESTAMP DEFAULT now()', 'created_date')
    add_column_if_missing('user_qr_mpg', 'active_status BOOLEAN DEFAULT TRUE', 'active_status')


def downgrade() -> None:
    # Non-destructive downgrade omitted to preserve data
    pass


