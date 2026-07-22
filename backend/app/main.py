from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import attendance, calendar, company, dashboard, session, simulation
from app.config import get_settings
from app.database import init_db

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    # In sviluppo crea le tabelle automaticamente. In produzione, preferire
    # migrazioni esplicite (es. Alembic) prima del deploy.
    init_db()
    yield


app = FastAPI(title="OfficePresence API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(session.router)
app.include_router(company.router)
app.include_router(dashboard.router)
app.include_router(attendance.router)
app.include_router(calendar.router)
app.include_router(simulation.router)


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok"}
