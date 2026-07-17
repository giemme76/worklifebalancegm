from tests.conftest import create_default_session


def test_create_attendance_requires_session(client):
    response = client.post("/attendance", json={"date": "2026-03-02", "type": "OFFICE"})
    assert response.status_code == 401


def test_create_attendance_returns_created_entry(client):
    create_default_session(client)

    response = client.post("/attendance", json={"date": "2026-03-02", "type": "OFFICE"})

    assert response.status_code == 201
    body = response.json()
    assert body["date"] == "2026-03-02"
    assert body["type"] == "OFFICE"
    assert body["is_simulated"] is False


def test_create_attendance_upserts_same_day(client):
    create_default_session(client)

    client.post("/attendance", json={"date": "2026-03-02", "type": "OFFICE"})
    response = client.post("/attendance", json={"date": "2026-03-02", "type": "SICK"})

    assert response.status_code == 201
    assert response.json()["type"] == "SICK"


def test_create_attendance_rejects_invalid_type(client):
    create_default_session(client)

    response = client.post("/attendance", json={"date": "2026-03-02", "type": "NOT_A_TYPE"})
    assert response.status_code == 422


def test_create_attendance_accepts_travel_type(client):
    create_default_session(client)

    response = client.post("/attendance", json={"date": "2026-03-02", "type": "TRAVEL"})
    assert response.status_code == 201
    assert response.json()["type"] == "TRAVEL"


def test_delete_attendance_removes_entry(client):
    create_default_session(client)
    client.post("/attendance", json={"date": "2026-03-02", "type": "OFFICE"})

    response = client.delete("/attendance/2026-03-02")
    assert response.status_code == 204

    calendar = client.get("/calendar", params={"year": 2026}).json()
    assert len(calendar["entries"]) == 0


def test_delete_attendance_missing_entry_returns_404(client):
    create_default_session(client)

    response = client.delete("/attendance/2026-03-02")
    assert response.status_code == 404


def test_delete_attendance_requires_session(client):
    response = client.delete("/attendance/2026-03-02")
    assert response.status_code == 401
