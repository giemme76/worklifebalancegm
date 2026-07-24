from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_session
from app.database import get_db
from app.models.session import UserSession
from app.schemas.company import (
    CompanyOut,
    CompanySearchResponse,
    CompanySearchResult,
    CompanySettingsUpdate,
)
from app.services.company_service import update_company_settings
from app.services.google_places_service import GooglePlacesError, search_companies

router = APIRouter(tags=["company"])


@router.get("/company", response_model=CompanyOut)
def read_company_settings(session: UserSession = Depends(get_current_session)) -> CompanyOut:
    """Impostazioni correnti dell'azienda (policy, giorni lavorativi, data di
    inizio monitoraggio), usate dalla sezione impostazioni della dashboard."""
    return session.company


@router.patch("/company", response_model=CompanyOut)
def update_company(
    data: CompanySettingsUpdate,
    session: UserSession = Depends(get_current_session),
    db: Session = Depends(get_db),
) -> CompanyOut:
    """Aggiorna policy e data di inizio monitoraggio dalla sezione impostazioni."""
    return update_company_settings(db, session, data)


@router.get("/company/search", response_model=CompanySearchResponse)
def search_company(q: str = Query(min_length=2, description="Nome azienda da cercare")) -> CompanySearchResponse:
    """Ricerca aziende reali tramite Google Places, usata in onboarding per far
    scegliere all'utente la propria sede tra risultati veri (invece di un
    valore inventato lato client)."""
    try:
        raw_results = search_companies(q)
    except GooglePlacesError as exc:
        # Onboarding resta utilizzabile anche se Google Places non risponde:
        # l'utente può comunque proseguire inserendo i dati a mano. Il
        # messaggio d'errore (status Google + error_message, mai la chiave)
        # torna comunque al client per diagnosticare senza dover leggere i
        # log del server.
        return CompanySearchResponse(results=[], error=str(exc))
    return CompanySearchResponse(results=[CompanySearchResult(**result) for result in raw_results])
