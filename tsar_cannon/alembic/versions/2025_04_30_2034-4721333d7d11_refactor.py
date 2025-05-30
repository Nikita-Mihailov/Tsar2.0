"""refactor

Revision ID: 4721333d7d11
Revises: 5d9f32a937e1
Create Date: 2025-04-30 20:34:56.597840

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4721333d7d11'
down_revision: Union[str, None] = '5d9f32a937e1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('clients', 'is_superuser',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('clients', 'is_superuser',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    # ### end Alembic commands ###
