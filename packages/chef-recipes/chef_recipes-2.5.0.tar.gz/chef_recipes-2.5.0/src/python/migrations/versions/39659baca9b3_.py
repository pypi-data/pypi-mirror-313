"""Add favorite field.

Revision ID: 39659baca9b3
Revises: 998321576878
Create Date: 2023-06-30 14:44:00.330099

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '39659baca9b3'
down_revision = '998321576878'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('recipe', sa.Column('favorite', sa.Boolean(), server_default=sa.false()))


def downgrade() -> None:
    op.drop_column('recipe', 'favorite')
