"""Integrazione con Google Places API ("New") per la ricerca aziende.

Usata in due punti:
- endpoint interattivo `GET /company/search` (onboarding: l'utente digita il
  nome azienda e sceglie tra i risultati reali restituiti da Google);
- `company_lookup_service.lookup_company`, come fallback automatico quando
  l'utente non specifica un sito web, per proporre sede e sito plausibili.

Richiede `GOOGLE_MAPS_API_KEY` in ambiente. Se assente, le funzioni
restituiscono una lista vuota (nessuna eccezione): l'onboarding resta
utilizzabile anche senza integrazione configurata.
"""

import logging

import httpx

from app.config import get_settings

logger = logging.getLogger(__name__)

_PLACES_SEARCH_URL = "https://places.googleapis.com/v1/places:searchText"

# Chiediamo solo i campi che usiamo: riduce la fascia di prezzo Places API
# ("Text Search - Basic" invece di includere foto, orari, ecc.).
_FIELD_MASK = ",".join(
    [
        "places.id",
        "places.displayName",
        "places.formattedAddress",
        "places.addressComponents",
        "places.websiteUri",
        "places.rating",
        "places.location",
    ]
)

_REQUEST_TIMEOUT_SECONDS = 8.0


class GooglePlacesError(Exception):
    """Errore di rete/HTTP nella chiamata a Google Places."""


def _extract_city(place: dict) -> str | None:
    for component in place.get("addressComponents", []):
        if "locality" in component.get("types", []):
            return component.get("longText")
    # Fallback: alcuni comuni minori sono classificati come
    # "administrative_area_level_3" invece di "locality".
    for component in place.get("addressComponents", []):
        if "administrative_area_level_3" in component.get("types", []):
            return component.get("longText")
    return None


def _parse_place(place: dict) -> dict:
    location = place.get("location") or {}
    return {
        "place_id": place.get("id"),
        "name": (place.get("displayName") or {}).get("text"),
        "address": place.get("formattedAddress"),
        "city": _extract_city(place),
        "website": place.get("websiteUri"),
        "rating": place.get("rating"),
        "lat": location.get("latitude"),
        "lng": location.get("longitude"),
    }


def search_companies(query: str, *, region_code: str = "IT", max_results: int = 8) -> list[dict]:
    """Cerca aziende/sedi per nome tramite Google Places Text Search.

    Restituisce una lista di dict (place_id, name, address, city, website,
    rating, lat, lng). Lista vuota se la chiave API non è configurata o se
    Google non trova risultati.
    """
    settings = get_settings()
    if not settings.google_maps_api_key or not query.strip():
        return []

    try:
        response = httpx.post(
            _PLACES_SEARCH_URL,
            json={
                "textQuery": query,
                "regionCode": region_code,
                "maxResultCount": max_results,
            },
            headers={
                "Content-Type": "application/json",
                "X-Goog-Api-Key": settings.google_maps_api_key,
                "X-Goog-FieldMask": _FIELD_MASK,
            },
            timeout=_REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        # Logghiamo status + corpo della risposta di Google: è l'unico modo per
        # distinguere "chiave non valida", "API non abilitata sul progetto",
        # "billing disattivato" o "quota superata", che altrimenti l'endpoint
        # nasconde restituendo semplicemente una lista vuota.
        logger.warning(
            "Google Places ha risposto %s per query %r: %s",
            exc.response.status_code,
            query,
            exc.response.text[:1000],
        )
        raise GooglePlacesError(f"Errore chiamata Google Places: {exc}") from exc
    except httpx.HTTPError as exc:
        logger.warning("Errore di rete verso Google Places per query %r: %s", query, exc)
        raise GooglePlacesError(f"Errore chiamata Google Places: {exc}") from exc

    data = response.json()
    return [_parse_place(place) for place in data.get("places", [])]
