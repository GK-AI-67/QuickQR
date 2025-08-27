"""make non-id fields nullable in lost and found tables

Revision ID: c9d8e7f6a5b4
Revises: b7c8d9e0f1a2
Create Date: 2025-08-26 00:20:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql as psql


# revision identifiers, used by Alembic.
revision: str = 'c9d8e7f6a5b4'
down_revision: Union[str, Sequence[str], None] = 'b7c8d9e0f1a2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Drop NOT NULL constraints on non-id fields, only if those columns exist."""
    conn = op.get_bind()

    def drop_not_null_if_exists(table: str, column: str) -> None:
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
            {"t": table, "c": column},
        ).scalar()
        if exists:
            conn.execute(sa.text(f'ALTER TABLE "{table}" ALTER COLUMN "{column}" DROP NOT NULL'))

    # user_dtls
    for col in [
        "gmail",
        "first_name",
        "last_name",
        "password",
        "created_by",
        "last_logged_in_time",
        "active_status",
        "created_date",
        "provider",
    ]:
        drop_not_null_if_exists("user_dtls", col)

    # lost_and_found_qr (cover possible column sets across revisions)
    for col in [
        "name",
        "first_name",
        "last_name",
        "phone_number",
        "email",
        "address",
        "address_location",
        "description",
        "item_type",
        "is_found",
        "found_date",
        "found_location",
        "found_by_user_id",
        "create_date",
        "last_modified_date",
        "active_status",
        # legacy columns
        "item_name",
        "contact_info",
        "location",
        "created_at",
        "updated_at",
        "full_name",
        "company",
        "website",
        "send_location_on_scan",
        "user_id",
    ]:
        drop_not_null_if_exists("lost_and_found_qr", col)

    # lost_and_found_scanner
    for col in [
        "qrid",
        "userid",
        "scanned_qr_location",
        "scanned_ip_address",
        "scanned_user_agent",
        "scan_type",
        "action_taken",
        "create_date",
        "active_status",
    ]:
        drop_not_null_if_exists("lost_and_found_scanner", col)

    # user_qr_mpg
    for col in [
        "qrid",
        "userid",
        "scan_location",
        "scan_ip",
        "scan_user_agent",
        "scan_date",
        "is_first_scan",
        "details_updated",
        "created_date",
        "active_status",
    ]:
        drop_not_null_if_exists("user_qr_mpg", col)

    # qr_permission_dtls
    for col in [
        "qr_id",
        "field_name",
        "permission",
        "created_date",
        "last_modified_date",
        "active_status",
    ]:
        drop_not_null_if_exists("qr_permission_dtls", col)


def downgrade() -> None:
    # No-op: restoring NOT NULL blindly risks data loss; manual handling recommended.
    pass

