"""add client fields city phone2

Revision ID: 038c485d7b05
Revises: bc6b49af3547
Create Date: 2025-11-06 09:50:11.024071

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '038c485d7b05'
down_revision: Union[str, Sequence[str], None] = 'bc6b49af3547'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Agregar campos phone2 y city a la tabla clients
    op.add_column('clients', sa.Column('phone2', sa.String(), nullable=True))
    op.add_column('clients', sa.Column('city', sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    # Eliminar campos phone2 y city de la tabla clients
    op.drop_column('clients', 'city')
    op.drop_column('clients', 'phone2')
