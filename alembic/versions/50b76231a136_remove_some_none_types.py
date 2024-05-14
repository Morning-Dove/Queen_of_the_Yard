"""remove some None types

Revision ID: 50b76231a136
Revises: 960068e50467
Create Date: 2024-05-14 11:33:32.386801

"""
from typing import Sequence

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '50b76231a136'
down_revision: str | None = '960068e50467'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('servicearea', 'customerId',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('servicearea', 'customerId',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###