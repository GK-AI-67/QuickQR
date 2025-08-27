"""add created_date to user_dtls

Revision ID: 94a623a1bece
Revises: 95a88cff1004
Create Date: 2025-08-26 16:11:04.559358

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '94a623a1bece'
down_revision: Union[str, Sequence[str], None] = '95a88cff1004'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('user_dtls', sa.Column('created_date', sa.DateTime(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('user_dtls', 'created_date')
