"""Ricerca automatica (best-effort) di sito aziendale e sede principale.

Usa Google Places (vedi `google_places_service`) per proporre il primo
risultato plausibile quando l'utente non specifica un sito web in
onboarding. Se la chiave API non è configurata o Google non trova nulla,
ricade su un'euristica locale (slug del nome) senza sede suggerita, così
l'onboarding resta sempre utilizzabile.
"""

import re

from app.schemas.company import CompanyLookupResponse
from app.services.google_places_service import GooglePlacesError, search_companies

# Forme comuni di ragione sociale da rimuovere prima di generare lo slug
# (gestisce sia "S.r.l." puntato che "Srl"/"SpA" senza punti).
_LEGAL_SUFFIX_PATTERN = re.compile(
    r"\b(s\.r\.l\.?|s\.p\.a\.?|srl|spa|ltd|inc|gmbh)\b", re.IGNORECASE
)


def _slugify(name: str) -> str:
    without_suffix = _LEGAL_SUFFIX_PATTERN.sub("", name)
    tokens = re.findall(r"[a-zA-Z0-9]+", without_suffix.lower())
    return "".join(tokens) or "azienda"


def lookup_company(name: str) -> CompanyLookupResponse:
    """Propone sito e sede principale in base al primo risultato Google Places
    per il nome azienda. Se non disponibile, propone solo un dominio plausibile
    (nessuna sede: l'utente la conferma a mano)."""
    try:
        results = search_companies(name)
    except GooglePlacesError:
        results = []

    if results:
        best = results[0]
        website = best.get("website") or f"https://www.{_slugify(name)}.com"
        return CompanyLookupResponse(website=website, suggested_headquarters=best.get("city"))

    slug = _slugify(name)
    return CompanyLookupResponse(website=f"https://www.{slug}.com", suggested_headquarters=None)
