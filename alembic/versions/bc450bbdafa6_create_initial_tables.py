"""create initial tables

Revision ID: bc450bbdafa6
Revises: 
Create Date: 2025-10-24 14:43:15.121872

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bc450bbdafa6'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: crear tabla items si no existe."""
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    tables = inspector.get_table_names()
    if 'items' not in tables:
        op.create_table(
            'items',
            sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
            sa.Column('title', sa.String(), nullable=True),
            sa.Column('description', sa.String(), nullable=True),
            sa.Column('is_active', sa.Boolean(), nullable=True, server_default=sa.text('true')),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
            sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        )

        # Índices según el modelo
        op.create_index(op.f('ix_items_id'), 'items', ['id'], unique=False)
        op.create_index(op.f('ix_items_title'), 'items', ['title'], unique=False)


def downgrade() -> None:
    """Downgrade schema: eliminar tabla items e índices."""
    # Borrar índices si existen y luego la tabla
    try:
        op.drop_index(op.f('ix_items_title'), table_name='items')
    except Exception:
        pass
    try:
        op.drop_index(op.f('ix_items_id'), table_name='items')
    except Exception:
        pass
    try:
        op.drop_table('items')
    except Exception:
        pass
