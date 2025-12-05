"""
Alembic migration script to update the 'roletype' enum to use uppercase values and migrate existing data.
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'update_roletype_enum_uppercase'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Step 1: Rename old enum type
    op.execute("ALTER TYPE roletype RENAME TO roletype_old;")

    # Step 2: Create new enum type with uppercase values
    roletype_new = postgresql.ENUM('ADMIN', 'SUPERVISOR', 'COLLECTOR', name='roletype')
    roletype_new.create(op.get_bind())

    # Step 3: Alter column to use new enum type (cast text)
    op.execute("ALTER TABLE users ALTER COLUMN role DROP DEFAULT;")
    op.execute("ALTER TABLE users ALTER COLUMN role TYPE roletype USING UPPER(role)::text::roletype;")

    # Step 4: Drop old enum type
    op.execute("DROP TYPE roletype_old;")

def downgrade():
    # Step 1: Rename new enum type
    op.execute("ALTER TYPE roletype RENAME TO roletype_new;")

    # Step 2: Create old enum type with lowercase values
    roletype_old = postgresql.ENUM('admin', 'supervisor', 'collector', name='roletype')
    roletype_old.create(op.get_bind())

    # Step 3: Alter column to use old enum type (cast text)
    op.execute("ALTER TABLE users ALTER COLUMN role TYPE roletype USING LOWER(role)::text::roletype;")

    # Step 4: Drop new enum type
    op.execute("DROP TYPE roletype_new;")
