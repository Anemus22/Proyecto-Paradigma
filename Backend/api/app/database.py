import os
from pathlib import Path
from typing import Generator
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base, sessionmaker

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_SQLITE_PATH = BASE_DIR.parent.parent / "database" / "db.sqlite3"

raw_database_url = os.getenv("DB_POSTGRES", "").strip()
if raw_database_url.startswith("postgresql+asyncpg://"):
    raw_database_url = raw_database_url.replace("postgresql+asyncpg://", "postgresql+psycopg2://", 1)

SQLALCHEMY_DATABASE_URL = raw_database_url or f"sqlite:///{DEFAULT_SQLITE_PATH}"

connect_args = {}
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    connect_args=connect_args,
)

if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    @event.listens_for(Engine, "connect")
    def _set_sqlite_pragma(dbapi_connection, connection_record):
        try:
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()
        except Exception:
            pass

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
