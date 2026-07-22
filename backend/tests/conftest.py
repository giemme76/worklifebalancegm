from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import models  # noqa: F401  (registra i modelli su Base)
from app.database import Base, get_db
from app.main import app
from app.services import google_places_service


@pytest.fixture(autouse=True)
def _disable_google_places_by_default(monkeypatch):
    """Nessuna chiamata di rete reale nei test: senza questo, un `.env` locale
    con una chiave Google valida farebbe partire richieste HTTP vere durante
    la suite (es. via lookup_company in create_session). I test che vogliono
    verificare l'integrazione mockano esplicitamente search_companies/get_settings."""
    monkeypatch.setattr(
        google_places_service, "get_settings", lambda: SimpleNamespace(google_maps_api_key="")
    )


@pytest.fixture()
def db_session():
    """Sessione DB isolata per test, su SQLite in-memory."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    testing_session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = testing_session_local()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


@pytest.fixture()
def client(db_session):
    """TestClient con dependency override su get_db, verso lo stesso db_session."""

    def _override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = _override_get_db
    # Niente "with": evitiamo di eseguire il lifespan (init_db) sul DB reale,
    # dato che il DB usato nei test è quello di db_session.
    test_client = TestClient(app)
    yield test_client
    app.dependency_overrides.clear()


def create_default_session(client: TestClient, **overrides) -> dict:
    """Helper: crea una sessione con dati di default, restituisce il body della risposta."""
    payload = {
        "name": "Acme S.r.l.",
        "headquarters": "Milano",
        "smart_working_percentage": 40,
        "work_days_per_week": 5,
    }
    payload.update(overrides)
    response = client.post("/session", json=payload)
    assert response.status_code == 201, response.text
    return response.json()
