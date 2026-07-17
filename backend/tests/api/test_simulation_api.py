from tests.conftest import create_default_session


def test_simulation_requires_session(client):
    response = client.post("/simulation", json={"hypothetical_entries": []})
    assert response.status_code == 401


def test_simulation_projects_future_days_without_persisting(client):
    create_default_session(client)

    client.post("/attendance", json={"date": "2026-03-02", "type": "OFFICE"})

    response = client.post(
        "/simulation",
        json={
            "hypothetical_entries": [
                {"date": "2026-03-03", "type": "OFFICE"},
                {"date": "2026-03-04", "type": "OFFICE"},
            ]
        },
    )
    assert response.status_code == 200
    body = response.json()

    assert body["delta_office_days"] == 2
    assert body["projected"]["completed_office_days"] == 3

    # La simulazione non deve aver persistito nulla: la dashboard reale non cambia.
    dashboard = client.get("/dashboard", params={"year": 2026}).json()
    assert dashboard["completed_office_days"] == 1

    calendar = client.get("/calendar", params={"year": 2026}).json()
    assert len(calendar["entries"]) == 1
