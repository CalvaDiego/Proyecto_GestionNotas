"""Agregar tabla calificacion_promedio

Revision ID: afdb20b65c2d
Revises: 206ebc906d84
Create Date: 2025-02-10 02:12:39.647026

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'afdb20b65c2d'
down_revision: Union[str, None] = '206ebc906d84'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('calificacion_trimestre', sa.Column('id_calif_promedio', sa.Integer(), nullable=False))
    op.drop_index('ix_calificacion_trimestre_id_CalifPromedio', table_name='calificacion_trimestre')
    op.create_index(op.f('ix_calificacion_trimestre_id_calif_promedio'), 'calificacion_trimestre', ['id_calif_promedio'], unique=False)
    op.drop_column('calificacion_trimestre', 'id_CalifPromedio')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('calificacion_trimestre', sa.Column('id_CalifPromedio', sa.INTEGER(), autoincrement=True, nullable=False))
    op.drop_index(op.f('ix_calificacion_trimestre_id_calif_promedio'), table_name='calificacion_trimestre')
    op.create_index('ix_calificacion_trimestre_id_CalifPromedio', 'calificacion_trimestre', ['id_CalifPromedio'], unique=False)
    op.drop_column('calificacion_trimestre', 'id_calif_promedio')
    # ### end Alembic commands ###
