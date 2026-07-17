"""Logica di business per il calcolo di obiettivi, avanzamento e simulazioni.

Le funzioni qui dentro sono pure (nessun accesso al DB), per essere facilmente
testabili in isolamento.
"""

import calendar as _calendar_module
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date

from app.models.attendance import AttendanceType
from app.models.company import Company, PolicyType
from app.schemas.calendar import CalendarCounts
from app.schemas.dashboard import DashboardOut, Pace
from app.schemas.simulation import SimulationOut
from app.utils.date_utils import count_working_days_in_year

# Ferie, permessi, malattia e trasferta non contano né come presenza in ufficio
# né come smart working ai fini del calcolo dell'obiettivo.
_OTHER_TYPES = {
    AttendanceType.VACATION,
    AttendanceType.PERMIT,
    AttendanceType.SICK,
    AttendanceType.TRAVEL,
}


@dataclass(frozen=True)
class AnnualTarget:
    total_working_days: int
    required_office_days: int
    required_smart_days: int


def calculate_annual_target(company: Company, year: int) -> AnnualTarget:
    """Calcola i giorni lavorativi totali e la ripartizione richiesta ufficio/smart.

    Supporta entrambi i tipi di policy:
    - PERCENT: es. 40% smart working -> 60% presenza in ufficio
    - FIXED_DAYS: es. 3 giorni in ufficio a settimana
    """
    total_working_days = count_working_days_in_year(year, company.work_days_per_week)

    if company.policy_type == PolicyType.FIXED_DAYS:
        if company.office_days_per_week is None:
            raise ValueError("office_days_per_week mancante per policy FIXED_DAYS")
        working_weeks = total_working_days / company.work_days_per_week
        required_office_days = round(company.office_days_per_week * working_weeks)
    else:
        if company.smart_working_percentage is None:
            raise ValueError("smart_working_percentage mancante per policy PERCENT")
        office_percentage = 100 - company.smart_working_percentage
        required_office_days = round(total_working_days * office_percentage / 100)

    required_office_days = min(required_office_days, total_working_days)
    required_smart_days = total_working_days - required_office_days
    return AnnualTarget(
        total_working_days=total_working_days,
        required_office_days=required_office_days,
        required_smart_days=required_smart_days,
    )


def build_calendar_counts(attendance_types: Iterable[AttendanceType]) -> CalendarCounts:
    counts = CalendarCounts()
    for t in attendance_types:
        if t == AttendanceType.OFFICE:
            counts.office += 1
        elif t == AttendanceType.SMART_WORKING:
            counts.smart_working += 1
        elif t == AttendanceType.VACATION:
            counts.vacation += 1
        elif t == AttendanceType.PERMIT:
            counts.permit += 1
        elif t == AttendanceType.SICK:
            counts.sick += 1
        elif t == AttendanceType.TRAVEL:
            counts.travel += 1
    return counts


def _days_in_year(year: int) -> int:
    return 366 if _calendar_module.isleap(year) else 365


def _compute_pace(
    *, required_office_days: int, completed_office_days: int, year: int, as_of: date
) -> tuple[Pace, str]:
    """Semaforo di andamento, equivalente alla logica `getStats()` del design:

    confronta i giorni fatti con quelli attesi in base alla frazione di anno
    trascorsa, così da segnalare presto se si rischia di rimanere indietro.
    """
    jan1 = date(year, 1, 1)
    elapsed_days = (as_of - jan1).days + 1
    elapsed_fraction = min(1.0, max(0.0, elapsed_days / _days_in_year(year)))

    expected = required_office_days * elapsed_fraction
    ratio = (completed_office_days / expected) if expected > 0.5 else 1.0

    if completed_office_days >= required_office_days:
        return "green", "Obiettivo raggiunto"
    if ratio < 0.6:
        return "red", "Devi accelerare per recuperare"
    if ratio < 0.9:
        return "orange", "Rischi di rimanere indietro"
    return "green", "In linea con l'obiettivo"


def build_dashboard(
    company: Company,
    year: int,
    attendance_types: Iterable[AttendanceType],
    as_of: date | None = None,
) -> DashboardOut:
    """Calcola l'andamento rispetto all'obiettivo annuale in base alle presenze registrate."""
    target = calculate_annual_target(company, year)
    types = list(attendance_types)
    reference_date = as_of or date.today()

    completed_office_days = sum(1 for t in types if t == AttendanceType.OFFICE)
    completed_smart_days = sum(1 for t in types if t == AttendanceType.SMART_WORKING)
    other_days = sum(1 for t in types if t in _OTHER_TYPES)

    missing_office_days = max(target.required_office_days - completed_office_days, 0)

    accounted_days = completed_office_days + completed_smart_days
    if accounted_days > 0:
        current_office_percentage = (completed_office_days / accounted_days) * 100
        current_smart_percentage = 100 - current_office_percentage
    else:
        current_office_percentage = 0.0
        current_smart_percentage = 0.0

    pace, pace_label = _compute_pace(
        required_office_days=target.required_office_days,
        completed_office_days=completed_office_days,
        year=year,
        as_of=reference_date,
    )

    return DashboardOut(
        year=year,
        total_working_days=target.total_working_days,
        required_office_days=target.required_office_days,
        required_smart_days=target.required_smart_days,
        completed_office_days=completed_office_days,
        completed_smart_days=completed_smart_days,
        other_days=other_days,
        missing_office_days=missing_office_days,
        current_office_percentage=round(current_office_percentage, 2),
        current_smart_percentage=round(current_smart_percentage, 2),
        pace=pace,
        pace_label=pace_label,
        on_track=pace != "red",
    )


def simulate(
    company: Company,
    year: int,
    real_attendance_types: Iterable[AttendanceType],
    hypothetical_attendance_types: Iterable[AttendanceType],
    as_of: date | None = None,
) -> SimulationOut:
    """Calcola l'effetto di giorni futuri ipotetici sull'obiettivo, senza persistere nulla."""
    real_types = list(real_attendance_types)
    hypothetical_types = list(hypothetical_attendance_types)

    baseline = build_dashboard(company, year, real_types, as_of=as_of)
    projected = build_dashboard(company, year, real_types + hypothetical_types, as_of=as_of)

    return SimulationOut(
        projected=projected,
        delta_office_days=projected.completed_office_days - baseline.completed_office_days,
        delta_office_percentage=round(
            projected.current_office_percentage - baseline.current_office_percentage, 2
        ),
    )
