from datetime import date

from app.models.company import Company, PolicyType
from app.models.session import UserSession
from app.schemas.session import SessionCreateRequest
from app.services.session_service import create_session, delete_session, get_session_by_code
from app.utils.code_generator import generate_session_code, is_valid_code_format, normalize_code


def test_generate_session_code_format():
    code = generate_session_code()
    assert is_valid_code_format(code)
    assert code.startswith("SW-")
    assert len(code.split("-")) == 3


def test_generate_session_code_is_reasonably_unique():
    codes = {generate_session_code() for _ in range(200)}
    # Su un campione ragionevole non ci aspettiamo collisioni.
    assert len(codes) == 200


def test_create_session_generates_unique_code_and_company(db_session):
    data = SessionCreateRequest(
        name="Acme S.r.l.",
        smart_working_percentage=40,
        work_days_per_week=5,
    )
    session = create_session(db_session, data)

    assert is_valid_code_format(session.code)
    assert session.company.name == "Acme S.r.l."
    assert session.company.smart_working_percentage == 40


def test_create_session_stores_trimmed_nickname(db_session):
    data = SessionCreateRequest(
        name="Acme S.r.l.",
        nickname="  Guido  ",
        smart_working_percentage=40,
        work_days_per_week=5,
    )
    session = create_session(db_session, data)
    assert session.nickname == "Guido"


def test_create_session_blank_nickname_is_stored_as_none(db_session):
    data = SessionCreateRequest(
        name="Acme S.r.l.",
        nickname="   ",
        smart_working_percentage=40,
        work_days_per_week=5,
    )
    session = create_session(db_session, data)
    assert session.nickname is None


def test_create_session_without_nickname_is_none(db_session):
    data = SessionCreateRequest(
        name="Acme S.r.l.",
        smart_working_percentage=40,
        work_days_per_week=5,
    )
    session = create_session(db_session, data)
    assert session.nickname is None


def test_get_session_by_code_recupera_sessione_esistente(db_session):
    data = SessionCreateRequest(name="Beta SpA", smart_working_percentage=30, work_days_per_week=5)
    created = create_session(db_session, data)

    recovered = get_session_by_code(db_session, created.code)

    assert recovered is not None
    assert recovered.id == created.id
    assert recovered.code == created.code


def test_get_session_by_code_ritorna_none_per_codice_non_esistente(db_session):
    assert get_session_by_code(db_session, "SW-0000-0000") is None


def test_get_session_by_code_tollera_trattino_unicode_da_copia_incolla(db_session):
    # Autocorrect di editor/tabelle (Word, Notion, Google Sheets, "trattini
    # intelligenti" iOS/macOS) sostituisce spesso "-" con un en dash "–":
    # il recupero deve funzionare comunque, non solo con l'ASCII esatto.
    data = SessionCreateRequest(name="Acme S.r.l.", smart_working_percentage=40, work_days_per_week=5)
    created = create_session(db_session, data)
    pasted_code = created.code.replace("-", "–")  # noqa: RUF001 (en dash intenzionale)

    recovered = get_session_by_code(db_session, pasted_code)

    assert recovered is not None
    assert recovered.id == created.id


def test_get_session_by_code_tollera_minuscolo_e_spazi(db_session):
    data = SessionCreateRequest(name="Acme S.r.l.", smart_working_percentage=40, work_days_per_week=5)
    created = create_session(db_session, data)
    messy_code = f"  {created.code.lower()}  "

    recovered = get_session_by_code(db_session, messy_code)

    assert recovered is not None
    assert recovered.id == created.id


def test_normalize_code_replaces_dash_variants_and_uppercases():
    assert normalize_code("sw–j6r6–79vy") == "SW-J6R6-79VY"  # noqa: RUF001
    assert normalize_code("  SW-J6R6-79VY  ") == "SW-J6R6-79VY"
    assert normalize_code("SW - J6R6 - 79VY") == "SW-J6R6-79VY"


def test_create_session_defaults_monitoring_start_date_to_today(db_session):
    data = SessionCreateRequest(name="Acme S.r.l.", smart_working_percentage=40, work_days_per_week=5)
    session = create_session(db_session, data)
    assert session.company.monitoring_start_date == date.today()


def test_create_session_stores_chosen_monitoring_start_date(db_session):
    data = SessionCreateRequest(
        name="Acme S.r.l.",
        smart_working_percentage=40,
        work_days_per_week=5,
        monitoring_start_date=date(2026, 3, 15),
    )
    session = create_session(db_session, data)
    assert session.company.monitoring_start_date == date(2026, 3, 15)


def test_create_session_with_fixed_days_policy(db_session):
    data = SessionCreateRequest(
        name="Gamma Ltd",
        policy_type=PolicyType.FIXED_DAYS,
        office_days_per_week=3,
        work_days_per_week=5,
    )
    session = create_session(db_session, data)

    assert session.company.policy_type == PolicyType.FIXED_DAYS
    assert session.company.office_days_per_week == 3
    assert session.company.smart_working_percentage is None


def test_delete_session_removes_session_and_orphaned_company(db_session):
    data = SessionCreateRequest(name="Acme S.r.l.", smart_working_percentage=40, work_days_per_week=5)
    session = create_session(db_session, data)
    company_id = session.company_id

    delete_session(db_session, session)

    assert db_session.get(UserSession, session.id) is None
    assert db_session.get(Company, company_id) is None


def test_delete_session_keeps_company_if_other_sessions_remain(db_session):
    data = SessionCreateRequest(name="Acme S.r.l.", smart_working_percentage=40, work_days_per_week=5)
    session = create_session(db_session, data)
    company_id = session.company_id

    # Seconda sessione sulla stessa azienda (scenario futuro multi-persona).
    other = UserSession(code="SW-TEST-0001", company_id=company_id)
    db_session.add(other)
    db_session.commit()

    delete_session(db_session, session)

    assert db_session.get(UserSession, session.id) is None
    assert db_session.get(Company, company_id) is not None
    assert db_session.get(UserSession, other.id) is not None
