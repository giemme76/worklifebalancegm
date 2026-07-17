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
