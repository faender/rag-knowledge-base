from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.retrieval.search import similarity_search

router = APIRouter(tags=["ask"])


class AskRequest(BaseModel):
    question: str


@router.post("/ask")
def ask(payload: AskRequest):
    db: Session = SessionLocal()

    results = similarity_search(db, payload.question)

    db.close()

    return {"results": results}
