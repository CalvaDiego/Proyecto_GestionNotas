"""Recrear tabla actividad

Revision ID: 9d188df10019
Revises: c102c10b8da2
Create Date: 2025-02-03 20:14:03.032263

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9d188df10019'
down_revision: Union[str, None] = 'c102c10b8da2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('actividad',
    sa.Column('id_actividad', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(), nullable=False),
    sa.Column('tipo', sa.String(), nullable=False),
    sa.Column('id_trimestre', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_trimestre'], ['trimestre.id_trimestre'], ),
    sa.PrimaryKeyConstraint('id_actividad')
    )
    op.create_index(op.f('ix_actividad_id_actividad'), 'actividad', ['id_actividad'], unique=False)
    op.create_foreign_key(None, 'calificacion', 'actividad', ['id_actividad'], ['id_actividad'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'calificacion', type_='foreignkey')
    op.drop_index(op.f('ix_actividad_id_actividad'), table_name='actividad')
    op.drop_table('actividad')
    # ### end Alembic commands ###
