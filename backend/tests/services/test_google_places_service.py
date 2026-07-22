from types import SimpleNamespace

import httpx
import pytest

from app.services import google_places_service
from app.services.google_places_service import GooglePlacesError, search_companies


def _settings(api_key: str = "fake-key"):
    return SimpleNamespace(google_maps_api_key=api_key)


def test_search_companies_returns_empty_list_without_api_key(monkeypatch):
    monkeypatch.setattr(google_places_service, "get_settings", lambda: _settings(""))
    assert search_companies("Acme") == []


def test_search_companies_returns_empty_list_for_blank_query(monkeypatch):
    monkeypatch.setattr(google_places_service, "get_settings", lambda: _settings())
    assert search_companies("   ") == []


def test_search_companies_parses_google_response(monkeypatch):
    monkeypatch.setattr(google_places_service, "get_settings", lambda: _settings())

    fake_payload = {
        "places": [
            {
                "id": "abc123",
                "displayName": {"text": "Acme S.r.l."},
                "formattedAddress": "Via Roma 1, 20100 Milano MI, Italia",
                "addressComponents": [
                    {"longText": "Milano", "types": ["locality", "political"]},
                ],
                "websiteUri": "https://www.acme.it",
                "rating": 4.5,
                "location": {"latitude": 45.4642, "longitude": 9.19},
            }
        ]
    }

    class FakeResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return fake_payload

    def fake_post(url, json, headers, timeout):
        assert url == google_places_service._PLACES_SEARCH_URL
        assert json["textQuery"] == "Acme"
        assert headers["X-Goog-Api-Key"] == "fake-key"
        return FakeResponse()

    monkeypatch.setattr(google_places_service.httpx, "post", fake_post)

    results = search_companies("Acme")
    assert results == [
        {
            "place_id": "abc123",
            "name": "Acme S.r.l.",
            "address": "Via Roma 1, 20100 Milano MI, Italia",
            "city": "Milano",
            "website": "https://www.acme.it",
            "rating": 4.5,
            "lat": 45.4642,
            "lng": 9.19,
        }
    ]


def test_search_companies_falls_back_to_admin_area_when_no_locality(monkeypatch):
    monkeypatch.setattr(google_places_service, "get_settings", lambda: _settings())

    fake_payload = {
        "places": [
            {
                "id": "xyz",
                "displayName": {"text": "Beta"},
                "addressComponents": [
                    {"longText": "Comune Minore", "types": ["administrative_area_level_3"]},
                ],
            }
        ]
    }

    class FakeResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return fake_payload

    monkeypatch.setattr(
        google_places_service.httpx, "post", lambda *a, **k: FakeResponse()
    )

    results = search_companies("Beta")
    assert results[0]["city"] == "Comune Minore"
    assert results[0]["website"] is None
    assert results[0]["lat"] is None


def test_search_companies_raises_google_places_error_on_http_failure(monkeypatch):
    monkeypatch.setattr(google_places_service, "get_settings", lambda: _settings())

    def fake_post(*args, **kwargs):
        raise httpx.ConnectError("boom")

    monkeypatch.setattr(google_places_service.httpx, "post", fake_post)

    with pytest.raises(GooglePlacesError):
        search_companies("Acme")
