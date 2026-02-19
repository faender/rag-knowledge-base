"""change embedding dim to 384

Revision ID: 198c0a2dda8b
Revises: eb759701b485
Create Date: 2026-02-19 10:12:07.433263

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '198c0a2dda8b'
down_revision: Union[str, Sequence[str], None] = 'eb759701b485'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TABLE chunks ALTER COLUMN embedding TYPE vector(384);")

def downgrade() -> None:
    op.execute("ALTER TABLE chunks ALTER COLUMN embedding TYPE vector(1536);")
