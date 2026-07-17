from datetime import date

from app.models.attendance import AttendanceType
from app.models.company import Company
from app.models.session import UserSession
from app.repositories.attendance_repository import AttendanceRepository


def make_session(db_session) -> UserSession:
    company = Company(name="Acme", smart_working_percentage=40, work_days_per_week=5)
    db_session.add(company)
    db_session.flush()

    session = UserSession(code="SW-TEST-0001", company_id=company.id)
    db_session.add(session)
    db_session.flush()
    return session


def test_upsert_creates_new_entry(db_session):
    session = make_session(db_session)
    repo = AttendanceRepository(db_session)

    entry = repo.upsert(session.id, date(2026, 3, 2), AttendanceType.OFFICE)

    assert entry.id is not None
    assert entry.type == AttendanceType.OFFICE


def test_upsert_updates_existing_entry_for_same_day(db_session):
    session = make_session(db_session)
    repo = AttendanceRepository(db_session)

    first = repo.upsert(session.id, date(2026, 3, 2), AttendanceType.OFFICE)
    second = repo.upsert(session.id, date(2026, 3, 2), AttendanceType.SMART_WORKING)

    assert first.id == second.id
    entries = repo.list_for_year(session.id, 2026)
    assert len(entries) == 1
    assert entries[0].type == AttendanceType.SMART_WORKING


def test_list_for_year_excludes_simulated_by_default(db_session):
    session = make_session(db_session)
    repo = AttendanceRepository(db_session)

    repo.upsert(session.id, date(2026, 3, 2), AttendanceType.OFFICE, is_simulated=False)
    repo.upsert(session.id, date(2026, 3, 3), AttendanceType.OFFICE, is_simulated=True)

    real_only = repo.list_for_year(session.id, 2026, include_simulated=False)
    with_simulated = repo.list_for_year(session.id, 2026, include_simulated=True)

    assert len(real_only) == 1
    assert len(with_simulated) == 2


def test_list_for_year_filters_by_year(db_session):
    session = make_session(db_session)
    repo = AttendanceRepository(db_session)

    repo.upsert(session.id, date(2025, 12, 31), AttendanceType.OFFICE)
    repo.upsert(session.id, date(2026, 1, 2), AttendanceType.OFFICE)

    assert len(repo.list_for_year(session.id, 2025)) == 1
    assert len(repo.list_for_year(session.id, 2026)) == 1
