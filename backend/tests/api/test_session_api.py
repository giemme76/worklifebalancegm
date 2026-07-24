from tests.conftest import create_default_session


def test_create_session_returns_code_and_sets_cookie(client):
    body = create_default_session(client)

    assert body["code"].startswith("SW-")
    assert body["company"]["name"] == "Acme S.r.l."
    assert body["company"]["smart_working_percentage"] == 40

    # Il cookie di sessione deve essere stato impostato dal server.
    assert client.cookies.get("officepresence_session") == body["code"]


def test_create_session_stores_and_returns_nickname(client):
    body = create_default_session(client, nickname="Guido")
    assert body["nickname"] == "Guido"


def test_create_session_nickname_is_optional(client):
    body = create_default_session(client)
    assert body["nickname"] is None


def test_create_session_trims_blank_nickname_to_none(client):
    body = create_default_session(client, nickname="   ")
    assert body["nickname"] is None


def test_create_session_rejects_nickname_longer_than_ten_chars(client):
    response = client.post(
        "/session",
        json={
            "name": "Acme",
            "nickname": "NomeMoltoLungo",
            "smart_working_percentage": 40,
            "work_days_per_week": 5,
        },
    )
    assert response.status_code == 422


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


def test_recover_session_tolerates_unicode_dash_from_copy_paste(client):
    created = create_default_session(client)
    client.cookies.clear()
    # es. incollato da una tabella con "trattini intelligenti" attivi.
    pasted_code = created["code"].replace("-", "–")  # noqa: RUF001

    response = client.get(f"/session/{pasted_code}")

    assert response.status_code == 200
    assert response.json()["code"] == created["code"]


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


def test_create_session_with_fixed_days_policy(client):
    response = client.post(
        "/session",
        json={
            "name": "Gamma Ltd",
            "policy_type": "FIXED_DAYS",
            "office_days_per_week": 3,
            "work_days_per_week": 5,
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["company"]["policy_type"] == "FIXED_DAYS"
    assert body["company"]["office_days_per_week"] == 3


def test_create_session_fixed_days_requires_office_days_per_week(client):
    response = client.post(
        "/session",
        json={"name": "Gamma Ltd", "policy_type": "FIXED_DAYS", "work_days_per_week": 5},
    )
    assert response.status_code == 422


def test_read_current_session_bootstrap_from_cookie(client):
    created = create_default_session(client)

    response = client.get("/session")

    assert response.status_code == 200
    assert response.json()["code"] == created["code"]


def test_read_current_session_without_cookie_is_unauthorized(client):
    response = client.get("/session")
    assert response.status_code == 401


def test_delete_current_session_removes_it_and_clears_cookie(client):
    create_default_session(client)

    response = client.delete("/session")
    assert response.status_code == 204

    # La sessione non è più valida: la cookie è stata rimossa dal server e in
    # ogni caso il codice non risolve più a nulla.
    assert client.cookies.get("officepresence_session") is None
    assert client.get("/session").status_code == 401


def test_delete_current_session_without_cookie_is_unauthorized(client):
    response = client.delete("/session")
    assert response.status_code == 401
