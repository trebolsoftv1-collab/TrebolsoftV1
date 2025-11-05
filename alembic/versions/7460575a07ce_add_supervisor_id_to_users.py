"""add_supervisor_id_to_users

Revision ID: 7460575a07ce
Revises: 0edabb2f41d7
Create Date: 2025-11-05 10:05:34.200405

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7460575a07ce'
down_revision: Union[str, Sequence[str], None] = '0edabb2f41d7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: Add supervisor_id column to users table."""
    # Check if column exists before adding (idempotent)
    from sqlalchemy import inspect
    bind = op.get_bind()
    inspector = inspect(bind)
    
    columns = [col['name'] for col in inspector.get_columns('users')]
    
    if 'supervisor_id' not in columns:
        op.add_column('users', sa.Column('supervisor_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=True))


def downgrade() -> None:
    """Downgrade schema: Remove supervisor_id column from users table."""
    # Check if column exists before dropping
    from sqlalchemy import inspect
    bind = op.get_bind()
    inspector = inspect(bind)
    
    columns = [col['name'] for col in inspector.get_columns('users')]
    
    if 'supervisor_id' in columns:
        op.drop_column('users', 'supervisor_id')
