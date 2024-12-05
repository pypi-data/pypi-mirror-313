"""Add Timestamps

Revision ID: e454e6860914
Revises: ea9e0ff5a7ff
Create Date: 2024-12-03 11:48:10.519678

"""
from datetime import datetime

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'e454e6860914'
down_revision = 'ea9e0ff5a7ff'
branch_labels = None
depends_on = None

tables = ("category", "ingredient", "ingredient_item", "recipe", "tag", "unit")
columns = ("created_at", "updated_at")

def upgrade() -> None:
    # ADD COLS
    for table in tables:
        with op.batch_alter_table(table) as batch_op:
            for col in columns:
                batch_op.add_column(sa.Column(col, sa.DateTime(), nullable=True))

    # DATA MIGRATION
    for table in tables:
        set_clause = ", ".join([f"{col} = '{datetime.utcnow()}'" for col in columns])
        op.execute(f"UPDATE {table} SET {set_clause}")

    # SET TO NONNULL
    for table in tables:
        with op.batch_alter_table(table) as batch_op:
            for col in columns:
                batch_op.alter_column(col, nullable=False)


def downgrade() -> None:
    for table in tables:
        with op.batch_alter_table(table) as batch_op:
            for col in columns:
                batch_op.drop_column(col)
