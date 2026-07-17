"""Logica di business per il calcolo di obiettivi, avanzamento e simulazioni.

Le funzioni qui dentro sono pure (nessun accesso al DB), per essere facilmente
testabili in isolamento.
"""

from collections.abc import Iterable
from dataclasses import dataclass

from app.models.attendance import AttendanceType
from app.models.company import Company
from app.schemas.calendar import CalendarCounts
from app.schemas.dashboard import DashboardOut
from app.schemas.simulation import SimulationOut
from app.utils.date_utils import count_working_days_in_year

_OTHER_TYPES = {AttendanceType.VACATION, AttendanceType.PERMIT, AttendanceType.SICK}


@dataclass(frozen=True)
class AnnualTarget:
    total_working_days: int
    required_office_days: int
    required_smart_days: int


def calculate_annual_target(company: Company, year: int) -> AnnualTarget:
    """Calcola i giorni lavorativi totali e la ripartizione richiesta ufficio/smart.

    Esempi (spec):
    - 40% smart working -> 60% presenza in ufficio
    - 60% smart working -> 40% presenza in ufficio
    """
    total_working_days = count_working_days_in_year(year, company.work_days_per_week)
    required_office_days = round(total_working_days * company.office_percentage / 100)
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
    return counts


def build_dashboard(
    company: Company, year: int, attendance_types: Iterable[AttendanceType]
) -> DashboardOut:
    """Calcola l'andamento rispetto all'obiettivo annuale in base alle presenze registrate."""
    target = calculate_annual_target(company, year)
    types = list(attendance_types)

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

    days_used = completed_office_days + completed_smart_days + other_days
    remaining_working_days = max(target.total_working_days - days_used, 0)

    # "On track" = è ancora matematicamente possibile raggiungere il target
    # entro i giorni lavorativi rimanenti nell'anno.
    on_track = missing_office_days <= remaining_working_days

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
        on_track=on_track,
    )


def simulate(
    company: Company,
    year: int,
    real_attendance_types: Iterable[AttendanceType],
    hypothetical_attendance_types: Iterable[AttendanceType],
) -> SimulationOut:
    """Calcola l'effetto di giorni futuri ipotetici sull'obiettivo, senza persistere nulla."""
    real_types = list(real_attendance_types)
    hypothetical_types = list(hypothetical_attendance_types)

    baseline = build_dashboard(company, year, real_types)
    projected = build_dashboard(company, year, real_types + hypothetical_types)

    return SimulationOut(
        projected=projected,
        delta_office_days=projected.completed_office_days - baseline.completed_office_days,
        delta_office_percentage=round(
            projected.current_office_percentage - baseline.current_office_percentage, 2
        ),
    )
