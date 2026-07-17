from datetime import date

from app.models.attendance import AttendanceType
from app.models.company import Company, PolicyType
from app.services import calculation_service
from app.utils.date_utils import count_working_days_in_year


def make_company(
    *,
    policy_type: PolicyType = PolicyType.PERCENT,
    smart_working_percentage: float | None = None,
    office_days_per_week: int | None = None,
    work_days_per_week: int = 5,
) -> Company:
    return Company(
        name="Test Co",
        policy_type=policy_type,
        smart_working_percentage=smart_working_percentage,
        office_days_per_week=office_days_per_week,
        work_days_per_week=work_days_per_week,
    )


def test_annual_target_40_percent_smart_means_60_percent_office():
    company = make_company(smart_working_percentage=40)
    target = calculation_service.calculate_annual_target(company, 2026)

    total = count_working_days_in_year(2026, 5)
    assert target.total_working_days == total
    assert target.required_office_days == round(total * 0.60)
    assert target.required_smart_days == total - target.required_office_days


def test_annual_target_60_percent_smart_means_40_percent_office():
    company = make_company(smart_working_percentage=60)
    target = calculation_service.calculate_annual_target(company, 2026)

    total = count_working_days_in_year(2026, 5)
    assert target.required_office_days == round(total * 0.40)
    assert target.required_smart_days == total - target.required_office_days


def test_annual_target_scales_with_work_days_per_week():
    company = make_company(smart_working_percentage=50, work_days_per_week=4)
    target = calculation_service.calculate_annual_target(company, 2026)

    total = count_working_days_in_year(2026, 4)
    assert target.total_working_days == total
    assert target.required_office_days == round(total * 0.50)


def test_annual_target_fixed_days_policy():
    company = make_company(
        policy_type=PolicyType.FIXED_DAYS, office_days_per_week=3, work_days_per_week=5
    )
    target = calculation_service.calculate_annual_target(company, 2026)

    total = count_working_days_in_year(2026, 5)
    working_weeks = total / 5
    assert target.required_office_days == round(3 * working_weeks)
    assert target.required_smart_days == total - target.required_office_days


def test_annual_target_fixed_days_never_exceeds_total_working_days():
    # 5 giorni ufficio su una settimana lavorativa di 5: tutto il tempo lavorativo è in ufficio.
    company = make_company(policy_type=PolicyType.FIXED_DAYS, office_days_per_week=5)
    target = calculation_service.calculate_annual_target(company, 2026)

    assert target.required_office_days == target.total_working_days
    assert target.required_smart_days == 0


def test_build_dashboard_counts_completed_and_missing_days():
    company = make_company(smart_working_percentage=40)  # 60% target ufficio
    types = [AttendanceType.OFFICE] * 10 + [AttendanceType.SMART_WORKING] * 5

    dashboard = calculation_service.build_dashboard(
        company, 2026, types, as_of=date(2026, 3, 1)
    )

    assert dashboard.completed_office_days == 10
    assert dashboard.completed_smart_days == 5
    assert dashboard.other_days == 0
    assert dashboard.missing_office_days == max(dashboard.required_office_days - 10, 0)
    assert dashboard.current_office_percentage == round(10 / 15 * 100, 2)


def test_build_dashboard_with_no_entries_early_in_year_is_on_track():
    company = make_company(smart_working_percentage=40)
    # Il 1° gennaio: la frazione di tempo trascorsa è talmente minima che
    # nessun giorno è ancora "atteso" (soglia expected > 0.5 non raggiunta).
    dashboard = calculation_service.build_dashboard(
        company, 2026, [], as_of=date(2026, 1, 1)
    )

    assert dashboard.completed_office_days == 0
    assert dashboard.completed_smart_days == 0
    assert dashboard.current_office_percentage == 0.0
    assert dashboard.pace == "green"
    assert dashboard.on_track is True


def test_build_dashboard_falls_behind_when_far_into_year_with_no_office_days():
    company = make_company(smart_working_percentage=0)  # 100% giorni richiesti in ufficio
    total = count_working_days_in_year(2026, 5)

    # Quasi tutti i giorni lavorativi già "usati" come ferie, a fine anno: impossibile recuperare.
    types = [AttendanceType.VACATION] * (total - 1)

    dashboard = calculation_service.build_dashboard(
        company, 2026, types, as_of=date(2026, 12, 20)
    )
    assert dashboard.missing_office_days > 0
    assert dashboard.pace == "red"
    assert dashboard.on_track is False


def test_build_dashboard_reaches_green_when_target_met():
    company = make_company(smart_working_percentage=40)
    target = calculation_service.calculate_annual_target(company, 2026)
    types = [AttendanceType.OFFICE] * target.required_office_days

    dashboard = calculation_service.build_dashboard(
        company, 2026, types, as_of=date(2026, 12, 31)
    )
    assert dashboard.missing_office_days == 0
    assert dashboard.pace == "green"
    assert dashboard.pace_label == "Obiettivo raggiunto"


def test_build_calendar_counts_including_travel():
    types = [
        AttendanceType.OFFICE,
        AttendanceType.OFFICE,
        AttendanceType.SMART_WORKING,
        AttendanceType.VACATION,
        AttendanceType.PERMIT,
        AttendanceType.SICK,
        AttendanceType.TRAVEL,
    ]
    counts = calculation_service.build_calendar_counts(types)

    assert counts.office == 2
    assert counts.smart_working == 1
    assert counts.vacation == 1
    assert counts.permit == 1
    assert counts.sick == 1
    assert counts.travel == 1


def test_travel_days_count_as_other_not_office_or_smart():
    company = make_company(smart_working_percentage=40)
    types = [AttendanceType.TRAVEL] * 3

    dashboard = calculation_service.build_dashboard(
        company, 2026, types, as_of=date(2026, 3, 1)
    )
    assert dashboard.completed_office_days == 0
    assert dashboard.completed_smart_days == 0
    assert dashboard.other_days == 3


def test_simulate_adds_hypothetical_office_days():
    company = make_company(smart_working_percentage=40)
    real_types = [AttendanceType.OFFICE] * 5 + [AttendanceType.SMART_WORKING] * 5
    hypothetical_types = [AttendanceType.OFFICE] * 3

    result = calculation_service.simulate(
        company, 2026, real_types, hypothetical_types, as_of=date(2026, 3, 1)
    )

    assert result.delta_office_days == 3
    assert result.projected.completed_office_days == 8
    assert result.delta_office_percentage >= 0
