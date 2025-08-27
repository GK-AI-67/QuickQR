"""change lost_and_found_qr.user_id FK to user_dtls.userid and align type

Revision ID: g3h4i5j6k7l8
Revises: f2a3b4c5d6e7
Create Date: 2025-08-26 00:55:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'g3h4i5j6k7l8'
down_revision: Union[str, Sequence[str], None] = 'f2a3b4c5d6e7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()

    # Drop existing FK if it references users(id)
    conn.execute(sa.text(
        """
        DO $$
        DECLARE
            conname text;
        BEGIN
            SELECT tc.constraint_name INTO conname
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu
              ON tc.constraint_name = kcu.constraint_name
            JOIN information_schema.referential_constraints rc
              ON tc.constraint_name = rc.constraint_name
            JOIN information_schema.constraint_column_usage ccu
              ON ccu.constraint_name = rc.unique_constraint_name
            WHERE tc.table_schema = current_schema()
              AND tc.table_name = 'lost_and_found_qr'
              AND tc.constraint_type = 'FOREIGN KEY'
              AND ccu.table_name = 'users'
              AND ccu.column_name = 'id'
              AND kcu.column_name = 'user_id'
            LIMIT 1;
            IF conname IS NOT NULL THEN
                EXECUTE 'ALTER TABLE "lost_and_found_qr" DROP CONSTRAINT ' || conname;
            END IF;
        END$$;
        """
    ))

    # Align type to TEXT to match user_dtls.userid
    conn.execute(sa.text('ALTER TABLE "lost_and_found_qr" ALTER COLUMN user_id TYPE TEXT USING user_id::text'))

    # Clean up existing data: set user_id to NULL where it doesn't exist in user_dtls
    conn.execute(sa.text(
        """
        UPDATE "lost_and_found_qr" AS l
        SET user_id = NULL
        WHERE user_id IS NOT NULL
          AND NOT EXISTS (
            SELECT 1 FROM user_dtls u WHERE u.userid = l.user_id
          )
        """
    ))

    # Add FK to user_dtls(userid) if not already present
    conn.execute(sa.text(
        """
        DO $$
        DECLARE
            exists_fk boolean;
        BEGIN
            SELECT EXISTS (
                SELECT 1
                FROM information_schema.table_constraints tc
                JOIN information_schema.key_column_usage kcu
                  ON tc.constraint_name = kcu.constraint_name
                JOIN information_schema.referential_constraints rc
                  ON tc.constraint_name = rc.constraint_name
                JOIN information_schema.constraint_column_usage ccu
                  ON ccu.constraint_name = rc.unique_constraint_name
                WHERE tc.table_schema = current_schema()
                  AND tc.table_name = 'lost_and_found_qr'
                  AND tc.constraint_type = 'FOREIGN KEY'
                  AND ccu.table_name = 'user_dtls'
                  AND ccu.column_name = 'userid'
                  AND kcu.column_name = 'user_id'
            ) INTO exists_fk;
            IF NOT exists_fk THEN
                EXECUTE 'ALTER TABLE "lost_and_found_qr" ADD CONSTRAINT lost_and_found_qr_user_id_fkey FOREIGN KEY (user_id) REFERENCES user_dtls(userid) ON DELETE SET NULL';
            END IF;
        END$$;
        """
    ))


def downgrade() -> None:
    # Non-destructive; no automatic rollback of FK target
    pass


