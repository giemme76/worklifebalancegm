"""Setup SQLAlchemy: engine, sessionmaker, base dichiarativa e dependency FastAPI."""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import get_settings

settings = get_settings()

_connect_args = {"check_same_thread": False} if settings.is_sqlite else {}

engine = create_engine(settings.database_url, connect_args=_connect_args, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session, None, None]:
    """Dependency FastAPI: fornisce una sessione DB per singola richiesta."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Crea le tabelle se non esistono. In produzione preferire migrazioni esplicite."""
    from app import models  # noqa: F401  (import per registrare i modelli su Base)

    Base.metadata.create_all(bind=engine)
