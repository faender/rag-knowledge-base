"""create documents and chunks

Revision ID: eb759701b485
Revises: ID: f43b67e8fd89
Create Date: <egal>
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "eb759701b485"
down_revision = "f43b67e8fd89"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "documents",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("source", sa.String(length=1024), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )

    op.create_table(
        "chunks",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "document_id",
            sa.Integer(),
            sa.ForeignKey("documents.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("chunk_index", sa.Integer(), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )

    # pgvector Spalte nachträglich hinzufügen
    op.execute(
        "ALTER TABLE chunks ADD COLUMN embedding vector(384) NOT NULL;"
    )

    # Index für Vektorsuche
    op.execute(
        "CREATE INDEX IF NOT EXISTS chunks_embedding_ivfflat "
        "ON chunks USING ivfflat (embedding vector_cosine_ops) "
        "WITH (lists = 100);"
    )

def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS chunks_embedding_ivfflat;")
    op.execute("ALTER TABLE chunks DROP COLUMN embedding;")
    op.drop_table("chunks")
    op.drop_table("documents")
