from fastapi import APIRouter, Query

from app.schemas.company import CompanySearchResponse, CompanySearchResult
from app.services.google_places_service import GooglePlacesError, search_companies

router = APIRouter(tags=["company"])


@router.get("/company/search", response_model=CompanySearchResponse)
def search_company(q: str = Query(min_length=2, description="Nome azienda da cercare")) -> CompanySearchResponse:
    """Ricerca aziende reali tramite Google Places, usata in onboarding per far
    scegliere all'utente la propria sede tra risultati veri (invece di un
    valore inventato lato client)."""
    try:
        raw_results = search_companies(q)
    except GooglePlacesError:
        # Onboarding resta utilizzabile anche se Google Places non risponde:
        # l'utente può comunque proseguire inserendo i dati a mano.
        raw_results = []
    return CompanySearchResponse(results=[CompanySearchResult(**result) for result in raw_results])
