"""Ricerca automatica (best-effort) di sito aziendale e sede principale.

Implementazione attuale: euristica locale basata sul nome azienda, senza
chiamate esterne. In una versione futura questo servizio potrà integrare
una vera ricerca web o un provider tipo Clearbit/Companies House.
"""

import re

from app.schemas.company import CompanyLookupResponse

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
    """Propone un dominio plausibile. La sede principale non è ancora determinabile
    senza un'integrazione esterna: viene restituita None (l'utente la conferma a mano)."""
    slug = _slugify(name)
    return CompanyLookupResponse(website=f"https://www.{slug}.com", suggested_headquarters=None)
