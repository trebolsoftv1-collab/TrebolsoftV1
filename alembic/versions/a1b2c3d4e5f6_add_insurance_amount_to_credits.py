"""add_insurance_amount_to_credits

Revision ID: a1b2c3d4e5f6
Revises: 7460575a07ce
Create Date: 2025-11-05 18:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = '7460575a07ce'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add insurance_amount column to credits table (idempotent, SQLite-safe)."""
    from sqlalchemy import inspect
    bind = op.get_bind()
    inspector = inspect(bind)

    columns = [col['name'] for col in inspector.get_columns('credits')]
    if 'insurance_amount' not in columns:
        # SQLite-safe batch alter
        with op.batch_alter_table('credits', schema=None) as batch_op:
            batch_op.add_column(sa.Column('insurance_amount', sa.Float(), nullable=True))
        # Backfill to 0 where NULL
        op.execute("UPDATE credits SET insurance_amount = 0 WHERE insurance_amount IS NULL")


def downgrade() -> None:
    from sqlalchemy import inspect
    bind = op.get_bind()
    inspector = inspect(bind)

    columns = [col['name'] for col in inspector.get_columns('credits')]
    if 'insurance_amount' in columns:
        with op.batch_alter_table('credits', schema=None) as batch_op:
            batch_op.drop_column('insurance_amount')
