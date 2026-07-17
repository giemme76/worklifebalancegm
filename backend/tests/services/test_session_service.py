from app.schemas.session import SessionCreateRequest
from app.services.session_service import create_session, get_session_by_code
from app.utils.code_generator import generate_session_code, is_valid_code_format


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


def test_get_session_by_code_recupera_sessione_esistente(db_session):
    data = SessionCreateRequest(name="Beta SpA", smart_working_percentage=30, work_days_per_week=5)
    created = create_session(db_session, data)

    recovered = get_session_by_code(db_session, created.code)

    assert recovered is not None
    assert recovered.id == created.id
    assert recovered.code == created.code


def test_get_session_by_code_ritorna_none_per_codice_non_esistente(db_session):
    assert get_session_by_code(db_session, "SW-0000-0000") is None
