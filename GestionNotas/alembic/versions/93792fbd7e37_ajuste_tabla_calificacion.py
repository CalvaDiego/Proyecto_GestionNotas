"""Ajuste tabla Calificacion

Revision ID: 93792fbd7e37
Revises: 4b8433ff7d3e
Create Date: 2025-02-10 00:10:17.241762

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '93792fbd7e37'
down_revision: Union[str, None] = '4b8433ff7d3e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('calificacion_trimestre',
    sa.Column('id_trimestre_calif', sa.Integer(), nullable=False),
    sa.Column('id_estudiante', sa.Integer(), nullable=True),
    sa.Column('promedio_70', sa.Numeric(precision=5, scale=2), nullable=True),
    sa.Column('nota_proyecto', sa.Numeric(precision=5, scale=2), nullable=True),
    sa.Column('nota_evaluacion', sa.Numeric(precision=5, scale=2), nullable=True),
    sa.Column('promedio_30', sa.Numeric(precision=5, scale=2), nullable=True),
    sa.Column('nota_trimestre', sa.Numeric(precision=5, scale=2), nullable=True),
    sa.Column('promedio_cualitativo', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['id_estudiante'], ['estudiante.id_estudiante'], ),
    sa.PrimaryKeyConstraint('id_trimestre_calif')
    )
    op.create_index(op.f('ix_calificacion_trimestre_id_trimestre_calif'), 'calificacion_trimestre', ['id_trimestre_calif'], unique=False)
    op.create_table('calificacion_detalle',
    sa.Column('id_calificacion', sa.Integer(), nullable=False),
    sa.Column('id_estudiante', sa.Integer(), nullable=True),
    sa.Column('id_subactividad', sa.Integer(), nullable=True),
    sa.Column('nota_aporte', sa.Numeric(precision=5, scale=2), nullable=True),
    sa.ForeignKeyConstraint(['id_estudiante'], ['estudiante.id_estudiante'], ),
    sa.ForeignKeyConstraint(['id_subactividad'], ['subactividad.id_subactividad'], ),
    sa.PrimaryKeyConstraint('id_calificacion')
    )
    op.create_index(op.f('ix_calificacion_detalle_id_calificacion'), 'calificacion_detalle', ['id_calificacion'], unique=False)
    op.drop_index('ix_calificacion_id_calificacion', table_name='calificacion')
    op.drop_table('calificacion')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('calificacion',
    sa.Column('id_calificacion', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('id_estudiante', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('nota_aporte', sa.NUMERIC(precision=5, scale=2), autoincrement=False, nullable=True),
    sa.Column('nota_proyecto', sa.NUMERIC(precision=5, scale=2), autoincrement=False, nullable=True),
    sa.Column('nota_evaluacion', sa.NUMERIC(precision=5, scale=2), autoincrement=False, nullable=True),
    sa.Column('promedio_70', sa.NUMERIC(precision=5, scale=2), autoincrement=False, nullable=True),
    sa.Column('promedio_30', sa.NUMERIC(precision=5, scale=2), autoincrement=False, nullable=True),
    sa.Column('nota_trimestre', sa.NUMERIC(precision=5, scale=2), autoincrement=False, nullable=True),
    sa.Column('promedio_cualitativo', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('id_subactividad', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['id_estudiante'], ['estudiante.id_estudiante'], name='calificacion_id_estudiante_fkey'),
    sa.ForeignKeyConstraint(['id_subactividad'], ['subactividad.id_subactividad'], name='calificacion_id_subactividad_fkey'),
    sa.PrimaryKeyConstraint('id_calificacion', name='calificacion_pkey')
    )
    op.create_index('ix_calificacion_id_calificacion', 'calificacion', ['id_calificacion'], unique=False)
    op.drop_index(op.f('ix_calificacion_detalle_id_calificacion'), table_name='calificacion_detalle')
    op.drop_table('calificacion_detalle')
    op.drop_index(op.f('ix_calificacion_trimestre_id_trimestre_calif'), table_name='calificacion_trimestre')
    op.drop_table('calificacion_trimestre')
    # ### end Alembic commands ###
