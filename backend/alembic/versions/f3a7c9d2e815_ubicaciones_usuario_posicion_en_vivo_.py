"""ubicaciones_usuario: posicion en vivo del dispositivo (corrige D9)

Revision ID: f3a7c9d2e815
Revises: b11ca525ba46
Create Date: 2026-10-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import app.database.types


# revision identifiers, used by Alembic.
revision: str = 'f3a7c9d2e815'
down_revision: Union[str, None] = 'b11ca525ba46'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('ubicaciones_usuario',
    sa.Column('usuario_id', sa.Integer(), nullable=False),
    sa.Column('latitud', sa.Numeric(precision=9, scale=6), nullable=False),
    sa.Column('longitud', sa.Numeric(precision=9, scale=6), nullable=False),
    sa.Column('precision_m', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column('actualizado_en', app.database.types.UTCDateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['usuario_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('usuario_id')
    )


def downgrade() -> None:
    op.drop_table('ubicaciones_usuario')
