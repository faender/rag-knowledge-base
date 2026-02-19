from sqlalchemy import text
from sqlalchemy.orm import Session

from app.ingestion.embedder import embed_texts


def similarity_search(db: Session, query: str, k: int = 3):
    query_embedding = embed_texts([query])[0]

    sql = text("""
        SELECT
            c.id,
            c.chunk_index,
            c.text,
            d.id AS document_id,
            d.title AS document_title,
            d.source AS document_source,
            (c.embedding <=> (:embedding)::vector) AS distance
        FROM chunks c
        JOIN documents d ON d.id = c.document_id
        ORDER BY c.embedding <=> (:embedding)::vector
        LIMIT :k
    """)

    # Die Liste wird als String übergeben, passend zum ::vector Cast im SQL
    rows = db.execute(sql, {"embedding": str(query_embedding), "k": k}).fetchall()

    return [
        {
            "chunk_id": r.id,
            "chunk_index": r.chunk_index,
            "text": r.text,
            "distance": float(r.distance),
            "source": {
                "document_id": r.document_id,
                "title": r.document_title,
                "source": r.document_source,
            },
        }
        for r in rows
    ]
