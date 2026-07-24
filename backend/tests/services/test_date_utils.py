import calendar
from datetime import date, timedelta

from app.utils.date_utils import (
    count_working_days_in_range,
    count_working_days_in_year,
    working_weekdays,
)


def test_working_weekdays_five_days():
    assert working_weekdays(5) == {0, 1, 2, 3, 4}


def test_working_weekdays_clamped_between_1_and_7():
    assert working_weekdays(0) == {0}
    assert working_weekdays(10) == {0, 1, 2, 3, 4, 5, 6}


def _days_in_year(year: int) -> int:
    return 366 if calendar.isleap(year) else 365


def test_count_working_days_in_year_matches_weekday_count_five_days():
    year = 2026
    start = date(year, 1, 1)
    expected = sum(
        1
        for offset in range(_days_in_year(year))
        if (start + timedelta(days=offset)).weekday() < 5
    )
    assert count_working_days_in_year(year, 5) == expected


def test_count_working_days_in_year_seven_days_equals_days_in_year():
    year = 2026
    assert count_working_days_in_year(year, 7) == _days_in_year(year)


def test_count_working_days_in_range_matches_full_year_when_start_is_jan1():
    year = 2026
    assert count_working_days_in_range(date(year, 1, 1), date(year, 12, 31), 5) == (
        count_working_days_in_year(year, 5)
    )


def test_count_working_days_in_range_mid_year_is_smaller_than_full_year():
    year = 2026
    full = count_working_days_in_year(year, 5)
    partial = count_working_days_in_range(date(year, 7, 1), date(year, 12, 31), 5)
    assert 0 < partial < full


def test_count_working_days_in_range_empty_when_start_after_end():
    assert count_working_days_in_range(date(2026, 12, 31), date(2026, 1, 1), 5) == 0


def test_count_working_days_in_range_single_working_day():
    # Un lunedì singolo: 1 giorno lavorativo su settimana di 5.
    monday = date(2026, 3, 2)
    assert monday.weekday() == 0
    assert count_working_days_in_range(monday, monday, 5) == 1
