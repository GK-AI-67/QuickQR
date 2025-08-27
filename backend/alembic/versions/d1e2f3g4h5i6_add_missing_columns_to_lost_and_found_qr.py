"""add missing columns to lost_and_found_qr

Revision ID: d1e2f3g4h5i6
Revises: c9d8e7f6a5b4
Create Date: 2025-08-26 00:35:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd1e2f3g4h5i6'
down_revision: Union[str, Sequence[str], None] = 'c9d8e7f6a5b4'
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

    # Ensure pgcrypto available for defaults where used
    conn.execute(sa.text('CREATE EXTENSION IF NOT EXISTS "pgcrypto"'))

    # Add missing columns used by the application
    add_column_if_missing('lost_and_found_qr', 'name VARCHAR(255)', 'name')
    add_column_if_missing('lost_and_found_qr', 'user_id VARCHAR(255)', 'user_id')
    add_column_if_missing('lost_and_found_qr', 'first_name VARCHAR(255)', 'first_name')
    add_column_if_missing('lost_and_found_qr', 'last_name VARCHAR(255)', 'last_name')
    add_column_if_missing('lost_and_found_qr', 'phone_number VARCHAR(50)', 'phone_number')
    add_column_if_missing('lost_and_found_qr', 'email VARCHAR(255)', 'email')
    add_column_if_missing('lost_and_found_qr', 'address TEXT', 'address')
    add_column_if_missing('lost_and_found_qr', 'address_location VARCHAR(255)', 'address_location')
    add_column_if_missing('lost_and_found_qr', 'description TEXT', 'description')
    add_column_if_missing('lost_and_found_qr', 'item_type VARCHAR(100)', 'item_type')
    add_column_if_missing('lost_and_found_qr', 'is_found BOOLEAN DEFAULT FALSE', 'is_found')
    add_column_if_missing('lost_and_found_qr', 'found_date TIMESTAMP', 'found_date')
    add_column_if_missing('lost_and_found_qr', 'found_location VARCHAR(255)', 'found_location')
    add_column_if_missing('lost_and_found_qr', 'found_by_user_id VARCHAR(255)', 'found_by_user_id')
    add_column_if_missing('lost_and_found_qr', 'create_date TIMESTAMP DEFAULT now()', 'create_date')
    add_column_if_missing('lost_and_found_qr', 'last_modified_date TIMESTAMP', 'last_modified_date')
    add_column_if_missing('lost_and_found_qr', 'active_status BOOLEAN DEFAULT TRUE', 'active_status')

    # Ensure legacy primary key column "id" has a default to avoid insert failures when omitted
    id_exists = conn.execute(
        sa.text(
            """
            SELECT 1
            FROM information_schema.columns
            WHERE table_schema = current_schema()
              AND table_name = 'lost_and_found_qr'
              AND column_name = 'id'
            """
        )
    ).scalar()
    if id_exists:
        # Try to set a safe default if not present
        # Works whether id is text or uuid (uuid casts to text implicitly)
        conn.execute(sa.text('ALTER TABLE "lost_and_found_qr" ALTER COLUMN id SET DEFAULT gen_random_uuid()'))


def downgrade() -> None:
    # Non-destructive downgrade omitted to preserve data
    pass


