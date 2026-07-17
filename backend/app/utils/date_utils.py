"""Utility per il calcolo dei giorni lavorativi in un anno."""

from datetime import date, timedelta


def working_weekdays(work_days_per_week: int) -> set[int]:
    """Restituisce l'insieme degli indici weekday() (0=lunedì .. 6=domenica)
    considerati lavorativi, a partire dal lunedì.

    Esempio: work_days_per_week=5 -> {0,1,2,3,4} (lun-ven)
             work_days_per_week=4 -> {0,1,2,3} (lun-gio)
    """
    n = max(1, min(int(work_days_per_week), 7))
    return set(range(n))


def count_working_days_in_year(year: int, work_days_per_week: int) -> int:
    """Conta i giorni lavorativi nell'anno dato, in base ai giorni lavorativi/settimana."""
    valid_weekdays = working_weekdays(work_days_per_week)

    current = date(year, 1, 1)
    end = date(year, 12, 31)
    one_day = timedelta(days=1)

    count = 0
    while current <= end:
        if current.weekday() in valid_weekdays:
            count += 1
        current += one_day
    return count
