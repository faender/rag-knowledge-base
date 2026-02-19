from fastapi import APIRouter
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.db.models import Document, Chunk
from app.ingestion.chunker import simple_chunk
from app.ingestion.embedder import embed_texts

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/ingest_text")
def ingest_text(title: str, text: str):
    db: Session = SessionLocal()

    # Dokument erstellen
    document = Document(title=title)
    db.add(document)
    db.flush()  # erzeugt document.id

    # Chunking
    chunks = simple_chunk(text)

    # Embeddings erzeugen
    embeddings = embed_texts(chunks)

    for i, (chunk_text, embedding) in enumerate(zip(chunks, embeddings)):
        chunk = Chunk(
            document_id=document.id,
            chunk_index=i,
            text=chunk_text,
            embedding=embedding,
        )
        db.add(chunk)

    db.commit()
    db.close()

    return {"status": "ok", "chunks_created": len(chunks)}
