from tests.conftest import create_default_session


def test_calendar_requires_session(client):
    response = client.get("/calendar")
    assert response.status_code == 401


def test_calendar_counts_entries_by_type(client):
    create_default_session(client)

    entries = [
        ("2026-03-02", "OFFICE"),
        ("2026-03-03", "OFFICE"),
        ("2026-03-04", "SMART_WORKING"),
        ("2026-03-05", "VACATION"),
        ("2026-03-06", "PERMIT"),
        ("2026-03-09", "SICK"),
        ("2026-03-10", "TRAVEL"),
    ]
    for entry_date, entry_type in entries:
        client.post("/attendance", json={"date": entry_date, "type": entry_type})

    response = client.get("/calendar", params={"year": 2026})
    assert response.status_code == 200

    body = response.json()
    assert body["year"] == 2026
    assert len(body["entries"]) == 7
    assert body["counts"] == {
        "office": 2,
        "smart_working": 1,
        "vacation": 1,
        "permit": 1,
        "sick": 1,
        "travel": 1,
    }
