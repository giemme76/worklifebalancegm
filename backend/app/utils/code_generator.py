"""Generazione del codice univoco di sessione (es. SW-8F2K-7LQ9)."""

import re
import secrets

# Alfabeto senza caratteri facilmente confondibili (0/O, 1/I/L).
_ALPHABET = "23456789ABCDEFGHJKMNPQRSTUVWXYZ"
_GROUP_LENGTH = 4
_GROUPS = 2

# Varianti Unicode del trattino che autocorrect/editor (Word, Notion, Google
# Sheets, iOS/macOS "trattini intelligenti"...) sostituiscono al normale "-"
# quando l'utente copia il codice da una tabella o un documento. Se non
# normalizzate, il confronto esatto con il valore salvato (che usa sempre
# "-") fallisce silenziosamente e il recupero sessione risulta "non trovato"
# anche con un codice corretto.
_DASH_LIKE_CHARS = "‐‑‒–—―−"


def normalize_code(code: str) -> str:
    """Normalizza un codice inserito dall'utente prima del confronto in DB:
    spazi ai bordi, maiuscole, varianti Unicode del trattino e spazi attorno
    ai trattini (es. incollato come "SW - J6R6 - 79VY")."""
    normalized = code.strip().upper()
    for dash in _DASH_LIKE_CHARS:
        normalized = normalized.replace(dash, "-")
    normalized = re.sub(r"\s*-\s*", "-", normalized)
    return normalized


def _random_group(length: int = _GROUP_LENGTH) -> str:
    return "".join(secrets.choice(_ALPHABET) for _ in range(length))


def generate_session_code(prefix: str = "SW") -> str:
    """Genera un codice nel formato PREFIX-XXXX-XXXX, es. SW-8F2K-7LQ9."""
    groups = [_random_group() for _ in range(_GROUPS)]
    return "-".join([prefix, *groups])


def is_valid_code_format(code: str, prefix: str = "SW") -> bool:
    parts = code.split("-")
    if len(parts) != _GROUPS + 1:
        return False
    if parts[0] != prefix:
        return False
    return all(len(part) == _GROUP_LENGTH and all(c in _ALPHABET for c in part) for part in parts[1:])
