"""Restart from working state

Revision ID: 0e5355397ca1
Revises: 43e317e95d76
Create Date: 2024-05-15 14:09:21.290095

"""
from typing import Sequence

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '0e5355397ca1'
down_revision: str | None = '43e317e95d76'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###