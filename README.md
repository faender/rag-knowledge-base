```md
# RAG Knowledge Base (local)

Lokales RAG-Projekt (Retrieval-Augmented Generation) mit  
**FastAPI**, **PostgreSQL + pgvector** und **Alembic**.

Ziel des Projekts ist es, eine Knowledge Base aufzubauen, in die Dokumente
eingespielt werden können, um später belegte Antworten (mit Quellen)
auf Nutzerfragen zu generieren.

---

## Architektur (High-Level)

- **PostgreSQL (Docker)**  
  Speichert Dokumente, Text-Chunks und Vektor-Embeddings

- **Alembic**  
  Verwaltet das Datenbankschema (Extensions, Tabellen, Änderungen)

- **FastAPI + Uvicorn**  
  Stellt HTTP-Endpunkte bereit (z.B. `/ask`, `/health`)

---

## Voraussetzungen

- Linux / WSL
- Python 3.11+
- Docker + Docker Compose
- Docker Desktop (bei Windows + WSL)

---

## Projektstruktur (vereinfacht)

```

rag-knowledge-base/
├── app/
│   ├── main.py          # FastAPI App
│   └── db/
│       └── session.py   # DB-Verbindung
├── alembic/             # DB-Migrationen
├── docker-compose.yml   # Postgres + pgvector
├── .env.example         # ENV-Vorlage
├── .env                 # lokale ENV (nicht committen)
└── README.md

````

---

## Setup (einmalig)

### 1) Repository klonen
```bash
git clone <repo-url>
cd rag-knowledge-base
````

### 2) Python Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install fastapi uvicorn[standard] sqlalchemy psycopg[binary] alembic python-dotenv
```

### 3) Environment Variables

```bash
cp .env.example .env
```

* `.env` enthält lokale Konfiguration
* `.env` wird nicht committed
* `.env.example` dokumentiert benötigte Variablen

### 4) Database (Docker)

```bash
docker compose up -d
docker ps
```

### 5) Database Migrations (Alembic)

```bash
alembic upgrade head
```

> Alembic benötigt nur eine laufende Datenbank,
> der API-Server muss dafür nicht laufen.

### 6) Start API Server

```bash
uvicorn app.main:app --reload
```

Test:

* [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)
* [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Typical Development Flow

```bash
docker compose up -d
source .venv/bin/activate
alembic upgrade head
uvicorn app.main:app --reload
```

---

## Notes

* Alembic verwaltet ausschließlich das Datenbankschema
* FastAPI ist für HTTP/API zuständig
* PostgreSQL läuft isoliert in Docker

```
