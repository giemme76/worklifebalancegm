from tests.conftest import create_default_session


def test_create_session_returns_code_and_sets_cookie(client):
    body = create_default_session(client)

    assert body["code"].startswith("SW-")
    assert body["company"]["name"] == "Acme S.r.l."
    assert body["company"]["smart_working_percentage"] == 40

    # Il cookie di sessione deve essere stato impostato dal server.
    assert client.cookies.get("officepresence_session") == body["code"]


def test_recover_session_by_code(client):
    created = create_default_session(client)

    # Nuovo client "senza cookie": simula il recupero via codice su un altro browser.
    client.cookies.clear()
    response = client.get(f"/session/{created['code']}")

    assert response.status_code == 200
    assert response.json()["code"] == created["code"]


def test_recover_session_with_unknown_code_returns_404(client):
    response = client.get("/session/SW-0000-0000")
    assert response.status_code == 404


def test_create_session_validates_smart_working_percentage(client):
    response = client.post(
        "/session",
        json={
            "name": "Acme",
            "smart_working_percentage": 150,
            "work_days_per_week": 5,
        },
    )
    assert response.status_code == 422
