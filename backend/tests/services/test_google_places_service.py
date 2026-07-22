from types import SimpleNamespace

import httpx
import pytest

from app.services import google_places_service
from app.services.google_places_service import GooglePlacesError, search_companies


def _settings(api_key: str = "fake-key"):
    return SimpleNamespace(google_maps_api_key=api_key)


class FakeResponse:
    def __init__(self, payload):
        self._payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self._payload


def test_search_companies_returns_empty_list_without_api_key(monkeypatch):
    monkeypatch.setattr(google_places_service, "get_settings", lambda: _settings(""))
    assert search_companies("Acme") == []


def test_search_companies_returns_empty_list_for_blank_query(monkeypatch):
    monkeypatch.setattr(google_places_service, "get_settings", lambda: _settings())
    assert search_companies("   ") == []


def test_search_companies_parses_google_response(monkeypatch):
    monkeypatch.setattr(google_places_service, "get_settings", lambda: _settings())

    fake_payload = {
        "status": "OK",
        "results": [
            {
                "place_id": "abc123",
                "name": "Acme S.r.l.",
                "formatted_address": "Via Roma 1, 20100 Milano MI, Italia",
                "rating": 4.5,
                "geometry": {"location": {"lat": 45.4642, "lng": 9.19}},
            }
        ],
    }

    def fake_get(url, params, timeout):
        assert url == google_places_service._TEXT_SEARCH_URL
        assert params["query"] == "Acme"
        assert params["key"] == "fake-key"
        return FakeResponse(fake_payload)

    monkeypatch.setattr(google_places_service.httpx, "get", fake_get)

    results = search_companies("Acme")
    assert results == [
        {
            "place_id": "abc123",
            "name": "Acme S.r.l.",
            "address": "Via Roma 1, 20100 Milano MI, Italia",
            "city": "Milano",
            "website": None,
            "rating": 4.5,
            "lat": 45.4642,
            "lng": 9.19,
        }
    ]


def test_search_companies_returns_empty_list_for_zero_results(monkeypatch):
    monkeypatch.setattr(google_places_service, "get_settings", lambda: _settings())
    monkeypatch.setattr(
        google_places_service.httpx,
        "get",
        lambda *a, **k: FakeResponse({"status": "ZERO_RESULTS", "results": []}),
    )
    assert search_companies("Nonexistent") == []


def test_search_companies_returns_none_city_when_address_unparseable(monkeypatch):
    monkeypatch.setattr(google_places_service, "get_settings", lambda: _settings())
    fake_payload = {
        "status": "OK",
        "results": [
            {
                "place_id": "xyz",
                "name": "Beta",
                "formatted_address": "Indirizzo senza CAP riconoscibile",
            }
        ],
    }
    monkeypatch.setattr(google_places_service.httpx, "get", lambda *a, **k: FakeResponse(fake_payload))

    results = search_companies("Beta")
    assert results[0]["city"] is None
    assert results[0]["website"] is None
    assert results[0]["lat"] is None


def test_search_companies_raises_google_places_error_on_bad_status(monkeypatch):
    monkeypatch.setattr(google_places_service, "get_settings", lambda: _settings())
    monkeypatch.setattr(
        google_places_service.httpx,
        "get",
        lambda *a, **k: FakeResponse(
            {"status": "REQUEST_DENIED", "error_message": "API key invalid"}
        ),
    )
    with pytest.raises(GooglePlacesError):
        search_companies("Acme")


def test_search_companies_raises_google_places_error_on_http_failure(monkeypatch):
    monkeypatch.setattr(google_places_service, "get_settings", lambda: _settings())

    def fake_get(*args, **kwargs):
        raise httpx.ConnectError("boom")

    monkeypatch.setattr(google_places_service.httpx, "get", fake_get)

    with pytest.raises(GooglePlacesError):
        search_companies("Acme")
