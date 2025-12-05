"""Merge multiple heads

Revision ID: d42148f75b60
Revises: 038c485d7b05, update_roletype_enum_uppercase
Create Date: 2025-12-05 17:32:55.439553

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd42148f75b60'
down_revision: Union[str, Sequence[str], None] = ('038c485d7b05', 'update_roletype_enum_uppercase')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
