import calendar
from datetime import date, timedelta

from app.utils.date_utils import count_working_days_in_year, working_weekdays


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
