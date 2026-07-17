from datetime import date

from tests.conftest import create_default_session


def test_dashboard_requires_session_cookie(client):
    response = client.get("/dashboard")
    assert response.status_code == 401


def test_dashboard_returns_zeroed_progress_for_new_session(client):
    create_default_session(client, smart_working_percentage=40, work_days_per_week=5)

    # Anno futuro rispetto a "oggi": la frazione di anno trascorsa è zero,
    # quindi il target è sempre considerato raggiungibile ("on track").
    future_year = date.today().year + 1
    response = client.get("/dashboard", params={"year": future_year})

    assert response.status_code == 200
    body = response.json()
    assert body["completed_office_days"] == 0
    assert body["completed_smart_days"] == 0
    assert body["required_office_days"] > 0
    assert body["on_track"] is True
    assert body["pace"] == "green"


def test_dashboard_updates_after_recording_attendance(client):
    create_default_session(client, smart_working_percentage=40, work_days_per_week=5)

    client.post("/attendance", json={"date": "2026-03-02", "type": "OFFICE"})
    client.post("/attendance", json={"date": "2026-03-03", "type": "SMART_WORKING"})

    response = client.get("/dashboard", params={"year": 2026})
    body = response.json()

    assert body["completed_office_days"] == 1
    assert body["completed_smart_days"] == 1
