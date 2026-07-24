from datetime import date

from app.models.company import PolicyType
from app.schemas.company import CompanySettingsUpdate
from app.schemas.session import SessionCreateRequest
from app.services.company_service import update_company_settings
from app.services.session_service import create_session


def test_update_company_settings_changes_policy_and_monitoring_start_date(db_session):
    session = create_session(
        db_session,
        SessionCreateRequest(name="Acme S.r.l.", smart_working_percentage=40, work_days_per_week=5),
    )

    updated = update_company_settings(
        db_session,
        session,
        CompanySettingsUpdate(
            policy_type=PolicyType.FIXED_DAYS,
            office_days_per_week=3,
            work_days_per_week=5,
            monitoring_start_date=date(2026, 6, 1),
        ),
    )

    assert updated.policy_type == PolicyType.FIXED_DAYS
    assert updated.office_days_per_week == 3
    assert updated.smart_working_percentage is None
    assert updated.monitoring_start_date == date(2026, 6, 1)


def test_update_company_settings_persists_across_reload(db_session):
    session = create_session(
        db_session,
        SessionCreateRequest(name="Acme S.r.l.", smart_working_percentage=40, work_days_per_week=5),
    )
    company_id = session.company_id

    update_company_settings(
        db_session,
        session,
        CompanySettingsUpdate(
            policy_type=PolicyType.PERCENT,
            smart_working_percentage=25,
            work_days_per_week=5,
            monitoring_start_date=date(2026, 3, 1),
        ),
    )
    db_session.expire_all()

    from app.models.company import Company

    reloaded = db_session.get(Company, company_id)
    assert reloaded.smart_working_percentage == 25
    assert reloaded.monitoring_start_date == date(2026, 3, 1)
