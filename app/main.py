from fastapi import FastAPI
from app.db.session import db_smoke_test
from app.api.admin import router as admin_router
from app.api.ask import router as ask_router

app = FastAPI(title="RAG Knowledge Base")

app.include_router(admin_router)
app.include_router(ask_router)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/db")
def db():
    return db_smoke_test()
