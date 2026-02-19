"""enable pgvector extension

Revision ID: f43b67e8fd89
Revises: 
Create Date: 2026-02-18 13:33:33.731912

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f43b67e8fd89'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector;")

def downgrade() -> None:
    op.execute("DROP EXTENSION IF EXISTS vector;")
