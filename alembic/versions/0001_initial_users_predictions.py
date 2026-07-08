"""Initial schema: users and predictions tables.
Revision ID: 0001
Revises:
Create Date: 2026-06-30 12:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# Identificadores de revision
revision: str = '0001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Tabla de usuarios
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, autoincrement=True, nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False, unique=True),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('full_name', sa.String(length=255), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )   
    # Tabla de predicciones
    op.create_table(
        'predictions',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('input_data', sa.JSON(), nullable=False), # Features de entrada en formato JSON
        sa.Column('predicted_class', sa.Integer(), nullable=True),
        sa.Column('probability', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
    )
    # Indices adicionales
    op.create_index(op.f('ix_predictions_user_id'), 'predictions', ['user_id'])
    op.create_index(op.f('ix_users_email'), 'users', ['email'])

def downgrade() -> None:
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_predictions_user_id'), table_name='predictions')
    op.drop_table('predictions')
    op.drop_table('users')