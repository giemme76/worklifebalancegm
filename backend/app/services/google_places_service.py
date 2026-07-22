"""Integrazione con Google Places API (versione "legacy") per la ricerca aziende.

Usata in due punti:
- endpoint interattivo `GET /company/search` (onboarding: l'utente digita il
  nome azienda e sceglie tra i risultati reali restituiti da Google);
- `company_lookup_service.lookup_company`, come fallback automatico quando
  l'utente non specifica un sito web, per proporre sede e sito plausibili.

Usiamo la Places API "classica" (Text Search, `maps.googleapis.com/maps/api/
place/textsearch/json`) invece della più recente "Places API (New)": è quella
già abilitata sul progetto Google Cloud della chiave in uso (la stessa
condivisa con l'admin di energm), evitando di dover abilitare un secondo
prodotto Google separato. Il rovescio della medaglia: il Text Search legacy
non restituisce indirizzo strutturato né sito web, quindi la città viene
dedotta con un'euristica sull'indirizzo formattato e il sito resta a carico
del fallback su slug in `company_lookup_service`.

Richiede `GOOGLE_MAPS_API_KEY` in ambiente. Se assente, le funzioni
restituiscono una lista vuota (nessuna eccezione): l'onboarding resta
utilizzabile anche senza integrazione configurata.
"""

import logging
import re

import httpx

from app.config import get_settings

logger = logging.getLogger(__name__)

_TEXT_SEARCH_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"

_REQUEST_TIMEOUT_SECONDS = 8.0

# Indirizzi italiani formattati da Google hanno tipicamente la forma
# "Via Roma 1, 20100 Milano MI, Italia": catturiamo il testo tra il CAP
# (5 cifre) e la sigla provincia (2 lettere maiuscole).
_CITY_FROM_ADDRESS_PATTERN = re.compile(r"\b\d{5}\s+(.+?)\s+[A-Z]{2}\b")

# Status che rappresentano "nessun errore" per il Text Search legacy: una
# ricerca senza risultati non è un errore da segnalare come tale.
_OK_STATUSES = {"OK", "ZERO_RESULTS"}


class GooglePlacesError(Exception):
    """Errore di rete/HTTP/status nella chiamata a Google Places."""


def _extract_city(formatted_address: str | None) -> str | None:
    if not formatted_address:
        return None
    match = _CITY_FROM_ADDRESS_PATTERN.search(formatted_address)
    return match.group(1).strip() if match else None


def _parse_place(place: dict) -> dict:
    location = (place.get("geometry") or {}).get("location") or {}
    address = place.get("formatted_address")
    return {
        "place_id": place.get("place_id"),
        "name": place.get("name"),
        "address": address,
        "city": _extract_city(address),
        # Non disponibile nel Text Search legacy senza una chiamata aggiuntiva
        # a Place Details: il sito viene proposto altrove via slug fallback.
        "website": None,
        "rating": place.get("rating"),
        "lat": location.get("lat"),
        "lng": location.get("lng"),
    }


def search_companies(query: str, *, region_code: str = "it", max_results: int = 8) -> list[dict]:
    """Cerca aziende/sedi per nome tramite Google Places Text Search (legacy).

    Restituisce una lista di dict (place_id, name, address, city, website,
    rating, lat, lng). Lista vuota se la chiave API non è configurata o se
    Google non trova risultati.
    """
    settings = get_settings()
    if not settings.google_maps_api_key or not query.strip():
        return []

    try:
        response = httpx.get(
            _TEXT_SEARCH_URL,
            params={
                "query": query,
                "region": region_code,
                "key": settings.google_maps_api_key,
            },
            timeout=_REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
    except httpx.HTTPError as exc:
        logger.warning("Errore di rete verso Google Places per query %r: %s", query, exc)
        raise GooglePlacesError(f"Errore chiamata Google Places: {exc}") from exc

    data = response.json()
    status = data.get("status")
    if status not in _OK_STATUSES:
        # Logghiamo status + error_message: è l'unico modo per distinguere
        # "chiave non valida", "API non abilitata", "billing disattivato" o
        # "quota superata", che altrimenti l'endpoint nasconde restituendo
        # semplicemente una lista vuota.
        logger.warning(
            "Google Places ha risposto status=%s per query %r: %s",
            status,
            query,
            data.get("error_message"),
        )
        raise GooglePlacesError(f"Google Places status={status}: {data.get('error_message')}")

    return [_parse_place(place) for place in data.get("results", [])[:max_results]]
