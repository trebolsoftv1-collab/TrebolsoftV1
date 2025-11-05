"""add geolocation and photo to clients

Revision ID: d5e6f7g8h9i0
Revises: a1b2c3d4e5f6
Create Date: 2025-11-05 20:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd5e6f7g8h9i0'
down_revision: Union[str, Sequence[str], None] = 'a1b2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add latitude, longitude, and house_photo_url columns to clients table."""
    from sqlalchemy import inspect
    bind = op.get_bind()
    inspector = inspect(bind)

    columns = [col['name'] for col in inspector.get_columns('clients')]
    
    with op.batch_alter_table('clients', schema=None) as batch_op:
        if 'latitude' not in columns:
            batch_op.add_column(sa.Column('latitude', sa.Float(), nullable=True))
        if 'longitude' not in columns:
            batch_op.add_column(sa.Column('longitude', sa.Float(), nullable=True))
        if 'house_photo_url' not in columns:
            batch_op.add_column(sa.Column('house_photo_url', sa.String(), nullable=True))


def downgrade() -> None:
    """Remove geolocation and photo columns from clients table."""
    from sqlalchemy import inspect
    bind = op.get_bind()
    inspector = inspect(bind)

    columns = [col['name'] for col in inspector.get_columns('clients')]
    
    with op.batch_alter_table('clients', schema=None) as batch_op:
        if 'latitude' in columns:
            batch_op.drop_column('latitude')
        if 'longitude' in columns:
            batch_op.drop_column('longitude')
        if 'house_photo_url' in columns:
            batch_op.drop_column('house_photo_url')
