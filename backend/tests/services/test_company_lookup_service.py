from app.services import company_lookup_service
from app.services.company_lookup_service import lookup_company
from app.services.google_places_service import GooglePlacesError


def test_lookup_company_proposes_a_plausible_domain(monkeypatch):
    monkeypatch.setattr(company_lookup_service, "search_companies", lambda name: [])
    result = lookup_company("Acme S.r.l.")
    assert result.website == "https://www.acme.com"


def test_lookup_company_strips_non_alphanumeric_and_legal_suffixes(monkeypatch):
    monkeypatch.setattr(company_lookup_service, "search_companies", lambda name: [])
    result = lookup_company("Beta & Co. SpA")
    assert result.website == "https://www.betaco.com"


def test_lookup_company_headquarters_not_yet_determined_without_google_results(monkeypatch):
    monkeypatch.setattr(company_lookup_service, "search_companies", lambda name: [])
    result = lookup_company("Acme")
    assert result.suggested_headquarters is None


def test_lookup_company_uses_google_result_when_available(monkeypatch):
    monkeypatch.setattr(
        company_lookup_service,
        "search_companies",
        lambda name: [
            {"website": "https://www.acme.it", "city": "Milano"},
            {"website": "https://www.other.it", "city": "Roma"},
        ],
    )
    result = lookup_company("Acme S.r.l.")
    assert result.website == "https://www.acme.it"
    assert result.suggested_headquarters == "Milano"


def test_lookup_company_fills_missing_website_from_slug(monkeypatch):
    monkeypatch.setattr(
        company_lookup_service,
        "search_companies",
        lambda name: [{"website": None, "city": "Torino"}],
    )
    result = lookup_company("Acme S.r.l.")
    assert result.website == "https://www.acme.com"
    assert result.suggested_headquarters == "Torino"


def test_lookup_company_falls_back_to_slug_when_google_unavailable(monkeypatch):
    def _raise(name):
        raise GooglePlacesError("boom")

    monkeypatch.setattr(company_lookup_service, "search_companies", _raise)
    result = lookup_company("Acme S.r.l.")
    assert result.website == "https://www.acme.com"
    assert result.suggested_headquarters is None
