"""add is_admin to users

Revision ID: 0003
Revises: 0002
Create Date: 2026-07-02
"""

from alembic import op
import sqlalchemy as sa

revision: str = '0003'
down_revision: str = '0002'
branch_labels: None
depends_on: None

def upgrade():
    op.add_column('users', sa.Column('is_admin', sa.Boolean(), nullable=False, server_default='false'))

def downgrade():
    op.drop_column('users', 'is_admin')