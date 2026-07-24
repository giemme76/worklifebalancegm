"""Logica di business per il calcolo di obiettivi, avanzamento e simulazioni.

Le funzioni qui dentro sono pure (nessun accesso al DB), per essere facilmente
testabili in isolamento.
"""

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date

from app.models.attendance import AttendanceType
from app.models.company import Company, PolicyType
from app.schemas.calendar import CalendarCounts
from app.schemas.dashboard import DashboardOut, Pace
from app.schemas.simulation import SimulationOut
from app.utils.date_utils import count_working_days_in_range

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


def _monitoring_window(company: Company, year: int) -> tuple[date, date] | None:
    """Intervallo [inizio, fine] entro cui contare i giorni lavorativi nell'anno dato.

    Se `monitoring_start_date` non è impostata, o ricade in un anno precedente
    (il monitoraggio è già iniziato prima), l'intervallo è l'intero anno
    (comportamento storico). Se ricade in un anno futuro rispetto a `year`,
    il monitoraggio non è ancora iniziato in quell'anno: restituisce None.
    """
    start = company.monitoring_start_date
    year_start = date(year, 1, 1)
    year_end = date(year, 12, 31)

    if start is None or start.year < year:
        return year_start, year_end
    if start.year > year:
        return None
    return start, year_end


def calculate_annual_target(company: Company, year: int) -> AnnualTarget:
    """Calcola i giorni lavorativi totali e la ripartizione richiesta ufficio/smart.

    Supporta entrambi i tipi di policy:
    - PERCENT: es. 40% smart working -> 60% presenza in ufficio
    - FIXED_DAYS: es. 3 giorni in ufficio a settimana

    Se il monitoraggio non è ancora iniziato in `year` (vedi
    `monitoring_start_date`), l'obiettivo è zero.
    """
    window = _monitoring_window(company, year)
    if window is None:
        return AnnualTarget(total_working_days=0, required_office_days=0, required_smart_days=0)

    start, end = window
    total_working_days = count_working_days_in_range(start, end, company.work_days_per_week)

    if total_working_days == 0:
        return AnnualTarget(total_working_days=0, required_office_days=0, required_smart_days=0)

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


def _compute_pace(
    *, required_office_days: int, completed_office_days: int, start: date, end: date, as_of: date
) -> tuple[Pace, str]:
    """Semaforo di andamento, equivalente alla logica `getStats()` del design:

    confronta i giorni fatti con quelli attesi in base alla frazione già
    trascorsa della finestra di monitoraggio ([start, end], non
    necessariamente l'anno intero se è impostata una data di inizio), così da
    segnalare presto se si rischia di rimanere indietro.
    """
    if as_of < start:
        elapsed_fraction = 0.0
    else:
        total_days = (end - start).days + 1
        elapsed_days = (as_of - start).days + 1
        elapsed_fraction = min(1.0, max(0.0, elapsed_days / total_days))

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

    window = _monitoring_window(company, year)
    if window is None:
        # Il monitoraggio non è ancora iniziato in questo anno (data di inizio
        # nel futuro): nessun obiettivo attivo, niente da segnalare.
        pace, pace_label = "green", "Monitoraggio non ancora iniziato"
    else:
        start, end = window
        pace, pace_label = _compute_pace(
            required_office_days=target.required_office_days,
            completed_office_days=completed_office_days,
            start=start,
            end=end,
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
