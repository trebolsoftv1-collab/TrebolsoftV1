"""add phone and zone to users

Revision ID: bc6b49af3547
Revises: d5e6f7g8h9i0
Create Date: 2025-11-06 08:57:27.789226

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bc6b49af3547'
down_revision: Union[str, Sequence[str], None] = 'd5e6f7g8h9i0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Agregar campos phone y zone a la tabla users
    op.add_column('users', sa.Column('phone', sa.String(), nullable=True))
    op.add_column('users', sa.Column('zone', sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    # Eliminar campos phone y zone de la tabla users
    op.drop_column('users', 'zone')
    op.drop_column('users', 'phone')
