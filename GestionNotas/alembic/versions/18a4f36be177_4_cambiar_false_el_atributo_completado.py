"""4 Cambiar false el atributo completado

Revision ID: 18a4f36be177
Revises: d81d2764489b
Create Date: 2025-01-14 00:50:08.198112

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '18a4f36be177'
down_revision: Union[str, None] = 'd81d2764489b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
