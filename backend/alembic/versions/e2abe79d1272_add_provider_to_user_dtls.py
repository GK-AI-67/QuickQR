"""add provider to user_dtls

Revision ID: e2abe79d1272
Revises: 94a623a1bece
Create Date: 2025-08-26 16:14:20.893439

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e2abe79d1272'
down_revision: Union[str, Sequence[str], None] = '94a623a1bece'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('user_dtls', sa.Column('provider', sa.String(length=50), nullable=True))
    op.execute("UPDATE user_dtls SET provider = 'local' WHERE provider IS NULL")
    op.alter_column('user_dtls', 'provider', existing_type=sa.String(length=50), nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('user_dtls', 'provider')
