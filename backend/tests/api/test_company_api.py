from app.api import company as company_api
from tests.conftest import create_default_session


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


def test_search_company_returns_empty_results_and_error_message_when_google_fails(client, monkeypatch):
    def fake_search(query):
        raise company_api.GooglePlacesError("boom")

    monkeypatch.setattr(company_api, "search_companies", fake_search)

    response = client.get("/company/search", params={"q": "Acme"})
    assert response.status_code == 200
    body = response.json()
    assert body["results"] == []
    assert body["error"] == "boom"


def test_search_company_requires_min_length_query(client):
    response = client.get("/company/search", params={"q": "a"})
    assert response.status_code == 422


def test_read_company_settings_requires_session_cookie(client):
    response = client.get("/company")
    assert response.status_code == 401


def test_read_company_settings_returns_current_policy(client):
    create_default_session(client, smart_working_percentage=40, work_days_per_week=5)

    response = client.get("/company")

    assert response.status_code == 200
    body = response.json()
    assert body["policy_type"] == "PERCENT"
    assert body["smart_working_percentage"] == 40
    assert body["monitoring_start_date"] is not None


def test_update_company_settings_requires_session_cookie(client):
    response = client.patch(
        "/company",
        json={
            "policy_type": "PERCENT",
            "smart_working_percentage": 20,
            "work_days_per_week": 5,
            "monitoring_start_date": "2026-01-01",
        },
    )
    assert response.status_code == 401


def test_update_company_settings_changes_policy(client):
    create_default_session(client, smart_working_percentage=40, work_days_per_week=5)

    response = client.patch(
        "/company",
        json={
            "policy_type": "FIXED_DAYS",
            "office_days_per_week": 3,
            "work_days_per_week": 5,
            "monitoring_start_date": "2026-06-01",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["policy_type"] == "FIXED_DAYS"
    assert body["office_days_per_week"] == 3
    assert body["monitoring_start_date"] == "2026-06-01"

    # La modifica è visibile anche rileggendo le impostazioni.
    reread = client.get("/company")
    assert reread.json()["policy_type"] == "FIXED_DAYS"


def test_update_company_settings_validates_fixed_days_requires_office_days(client):
    create_default_session(client, smart_working_percentage=40, work_days_per_week=5)

    response = client.patch(
        "/company",
        json={
            "policy_type": "FIXED_DAYS",
            "work_days_per_week": 5,
            "monitoring_start_date": "2026-06-01",
        },
    )
    assert response.status_code == 422


def test_update_company_settings_reflects_in_dashboard(client):
    create_default_session(client, smart_working_percentage=40, work_days_per_week=5)

    client.patch(
        "/company",
        json={
            "policy_type": "PERCENT",
            "smart_working_percentage": 0,
            "work_days_per_week": 5,
            "monitoring_start_date": "2026-07-01",
        },
    )

    response = client.get("/dashboard", params={"year": 2026})
    assert response.status_code == 200
    body = response.json()
    # Con policy 100% ufficio e monitoraggio da luglio, il totale richiesto è
    # ridotto rispetto all'anno intero.
    assert body["required_office_days"] < 260
