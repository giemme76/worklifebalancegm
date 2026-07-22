from app.api import company as company_api


def test_search_company_returns_results_from_google(client, monkeypatch):
    def fake_search(query):
        assert query == "Acme"
        return [
            {
                "place_id": "abc123",
                "name": "Acme S.r.l.",
                "address": "Via Roma 1, Milano",
                "city": "Milano",
                "website": "https://www.acme.it",
                "rating": 4.5,
                "lat": 45.0,
                "lng": 9.0,
            }
        ]

    monkeypatch.setattr(company_api, "search_companies", fake_search)

    response = client.get("/company/search", params={"q": "Acme"})
    assert response.status_code == 200
    body = response.json()
    assert body["results"][0]["place_id"] == "abc123"
    assert body["results"][0]["city"] == "Milano"


def test_search_company_returns_empty_results_when_google_fails(client, monkeypatch):
    def fake_search(query):
        raise company_api.GooglePlacesError("boom")

    monkeypatch.setattr(company_api, "search_companies", fake_search)

    response = client.get("/company/search", params={"q": "Acme"})
    assert response.status_code == 200
    assert response.json() == {"results": []}


def test_search_company_requires_min_length_query(client):
    response = client.get("/company/search", params={"q": "a"})
    assert response.status_code == 422
