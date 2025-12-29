"""Add core models - users, clients, credits, transactions

Revision ID: 0edabb2f41d7
Revises: bc450bbdafa6
Create Date: 2025-10-24 15:04:33.444446

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0edabb2f41d7'
down_revision: Union[str, Sequence[str], None] = 'bc450bbdafa6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: crear users, clients, credits, cash_transactions si no existen."""
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    existing_tables = set(inspector.get_table_names())

    # Enums (PostgreSQL): crear tipos ENUM si no existen
    # (Bloque eliminado para evitar errores de indentación)

    # Definir enums para uso en create_table
    role_enum = sa.Enum('admin', 'supervisor', 'collector', name='roletype', create_type=True)
    credit_status_enum = sa.Enum('active', 'completed', 'defaulted', name='creditstatus', create_type=True)
    tx_type_enum = sa.Enum('payment', 'disbursement', 'deposit', 'withdrawal', name='transactiontype', create_type=True)

    # users
    if 'users' not in existing_tables:
        op.create_table(
            'users',
            sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
            sa.Column('email', sa.String(), nullable=False),
            sa.Column('username', sa.String(), nullable=False),
            sa.Column('hashed_password', sa.String(), nullable=False),
            sa.Column('full_name', sa.String(), nullable=True),
            sa.Column('role', role_enum, nullable=True),
            sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
            sa.Column('supervisor_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=True),
            sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=True),
            sa.Column('updated_at', sa.DateTime(), nullable=True),
        )
        # Índices y únicos
        op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
        op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
        op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)

    # clients
    if 'clients' not in existing_tables:
        op.create_table(
            'clients',
            sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
            sa.Column('dni', sa.String(), nullable=True),
            sa.Column('full_name', sa.String(), nullable=True),
            sa.Column('address', sa.String(), nullable=True),
            sa.Column('phone', sa.String(), nullable=True),
            sa.Column('email', sa.String(), nullable=True),
            sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
            sa.Column('collector_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=True),
            sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=True),
            sa.Column('updated_at', sa.DateTime(), nullable=True),
        )
        op.create_index(op.f('ix_clients_id'), 'clients', ['id'], unique=False)
        op.create_index(op.f('ix_clients_dni'), 'clients', ['dni'], unique=True)

    # credits
    if 'credits' not in existing_tables:
        op.create_table(
            'credits',
            sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
            sa.Column('client_id', sa.Integer(), sa.ForeignKey('clients.id'), nullable=True),
            sa.Column('amount', sa.Float(), nullable=True),
            sa.Column('interest_rate', sa.Float(), nullable=True),
            sa.Column('term_days', sa.Integer(), nullable=True),
            sa.Column('daily_payment', sa.Float(), nullable=True),
            sa.Column('total_amount', sa.Float(), nullable=True),
            sa.Column('remaining_amount', sa.Float(), nullable=True),
            sa.Column('status', credit_status_enum, nullable=True, server_default='active'),
            sa.Column('start_date', sa.DateTime(), server_default=sa.func.now(), nullable=True),
            sa.Column('end_date', sa.DateTime(), nullable=True),
            sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=True),
            sa.Column('updated_at', sa.DateTime(), nullable=True),
        )
        op.create_index(op.f('ix_credits_id'), 'credits', ['id'], unique=False)

    # cash_transactions
    if 'cash_transactions' not in existing_tables:
        op.create_table(
            'cash_transactions',
            sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
            sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=True),
            sa.Column('credit_id', sa.Integer(), sa.ForeignKey('credits.id'), nullable=True),
            sa.Column('amount', sa.Float(), nullable=True),
            sa.Column('transaction_type', tx_type_enum, nullable=True),
            sa.Column('description', sa.String(), nullable=True),
            sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=True),
            sa.Column('updated_at', sa.DateTime(), nullable=True),
        )
        op.create_index(op.f('ix_cash_transactions_id'), 'cash_transactions', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema: eliminar tablas e índices creados."""
    # Borrar en orden inverso por FKs
    # Eliminado el borrado de tablas e índices para evitar pérdida de datos
