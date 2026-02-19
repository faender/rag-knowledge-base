import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# 1) .env Datei laden (macht DATABASE_URL verfügbar)
load_dotenv()

# 2) DATABASE_URL aus Umgebungsvariablen lesen
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL fehlt. "
        "Hast du eine .env Datei angelegt?"
    )

# 3) SQLAlchemy Engine erstellen
# pool_pre_ping=True prüft Verbindungen automatisch
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

# 4) Session-Factory erstellen
# Jede Anfrage bekommt später ihre eigene Session
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

# 5) Smoke-Test (nur zum Testen, später optional entfernen)
def db_smoke_test() -> dict:
    """
    Testet, ob die DB erreichbar ist.
    Führt 'SELECT 1' aus.
    """
    with engine.connect() as conn:
        value = conn.execute(text("SELECT 1")).scalar_one()
        return {"select_1": value}
