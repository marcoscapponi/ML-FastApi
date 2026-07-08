""" Add useful columns to predictions table
Revision ID: 0002
Revises: 
Create Date: 2026-07-01 18:30:00
"""

from typing  import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '0002'
down_revision: Union[str, None] = '0001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # Agregar columnas a la tabla de predicciones
    op.add_column('predictions', sa.Column('class_names', sa.String(length=50), nullable=True))
    op.add_column('predictions', sa.Column('sepal_length', sa.Float(), nullable=True))
    op.add_column('predictions', sa.Column('sepal_width', sa.Float(), nullable=True))
    op.add_column('predictions', sa.Column('petal_length', sa.Float(), nullable=True))
    op.add_column('predictions', sa.Column('petal_width', sa.Float(), nullable=True))

    # Rellenar las nuevas columnas con datos existentes si es necesario
    connection = op.get_bind()

    # Asignar class_as_names basado en predicted_class
    connection.execute(sa.text("""
        UPDATE predictions
        SET class_names = CASE
            WHEN predicted_class = 0 THEN 'setosa'
            WHEN predicted_class = 1 THEN 'versicolor'
            WHEN predicted_class = 2 THEN 'virginica'
            ELSE 'unknown'
        END          
        """
    ))

    # Extraer características de input_data JSON y asignarlas a las nuevas columnas
    connection.execute(sa.text("""
        UPDATE predictions
        SET 
            sepal_length = CAST(input_data->'features'->>0 AS float),
            sepal_width = CAST(input_data->'features'->>1 AS float),
            petal_length = CAST(input_data->'features'->>2 AS float),
            petal_width = CAST(input_data->'features'->>3 AS float)
        """
    ))

    # Cambiar las columnas a NOT NULL si es necesario
    op.alter_column('predictions', 'class_names', nullable=False)
    op.alter_column('predictions', 'sepal_length', nullable=False)
    op.alter_column('predictions', 'sepal_width', nullable=False)
    op.alter_column('predictions', 'petal_length', nullable=False)
    op.alter_column('predictions', 'petal_width', nullable=False)

def downgrade():
    # Eliminar las columnas agregadas
    op.drop_column('predictions', 'class_names')
    op.drop_column('predictions', 'sepal_length')
    op.drop_column('predictions', 'sepal_width')
    op.drop_column('predictions', 'petal_length')
    op.drop_column('predictions', 'petal_width')