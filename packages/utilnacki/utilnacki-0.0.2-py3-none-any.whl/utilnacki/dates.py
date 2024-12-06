from datetime import date, datetime, timedelta
import pandas as pd

MIN_POSSIBLE_DATE, MAX_POSSIBLE_DATE = date(1900, 1, 1), date(2099, 12, 31)
NOW = datetime.now()
TODAY = date.today()
TIME_PERIODS = {
    'Last 30 Days': (TODAY - timedelta(days=30), TODAY),
    'Last Month': ((TODAY.replace(day=1) - timedelta(days=1)).replace(day=1), TODAY.replace(day=1) - timedelta(days=1)),
    'This Year': (date(TODAY.year, 1, 1), TODAY),
    'Last Year': (date(TODAY.year - 1, 1, 1), TODAY.replace(month=1, day=1) - timedelta(days=1)),
    'Last 365 Days': (TODAY - timedelta(days=365), TODAY),
    'All Dates': (MIN_POSSIBLE_DATE, MAX_POSSIBLE_DATE)
}

def to_datetime(d: date) -> datetime:
    return datetime.combine(d, datetime.min.time())

def every_date(dates_and_date_times: list[date | datetime]):
    """For a list of dates/date times, return a sorted list of every date between the earliest and latest
    date in the data, regardless if that date is present in the data.
    Example: ['2024-06-28', '2024-06-30', '2024-06-30'] -> ['2024-06-28', '2024-06-29', '2024-06-30'].
    The incoming list must have at least two elements"""
    if len(dates_and_date_times) < 2:
        raise ValueError('You must provide at least two dates or date-times')
    dates = [d.date() if isinstance(d, datetime) else d for d in dates_and_date_times]
    return [date_ts.date() for date_ts in pd.date_range(start=min(dates), end=max(dates))]


def _diff_count_and_unit(diff: timedelta) -> tuple[int, str]:
    """Return examples: (4, 'year'), (25, 'day'), (0, 'second')"""
    diff_str = str(diff)
    if diff.days < 1:
        hours, minutes, seconds = diff_str.split(':')
        h, m, s = int(hours), int(minutes), int(float(seconds))
        return (h, 'hour') if h > 1 else (m, 'minute') if m > 1 else (s, 'second')
    else:
        days_unit_str, _ = diff_str.split(',')
        days, _ = days_unit_str.split(' ')
        d = int(days)
        return (d // 365, 'year') if d >= 365 else (d // 30, 'month') if d >= 30 else (d, 'day')


def ago(d: date | datetime) -> str:
    """Return examples: '4 years ago', '2 months ago', '20 days ago', 'yesterday'.
    For durations less than one day, if the argument is a date, it will only return 'today' (due to no time info),
    if the arg is a date-time, example returns are: '18 hours ago', '1 minute ago', None
    Because the argument is not a time, it provides less sub-day specificity than ago_from_date_time."""
    # handle date-only items; convert to date-time
    if not isinstance(d, datetime):
        if d > TODAY:
            raise ValueError('You must supply a date/date-time in the past')
        if TODAY == d:
            return 'today'
        d = to_datetime(d)
    diff: timedelta = NOW - d
    if d > NOW:
        raise ValueError('You must supply a date/date-time in the past')
    if diff.days == 1:
        return 'yesterday'
    cnt, unit = _diff_count_and_unit(diff)
    return f'{cnt} {unit} ago' if cnt == 1 else f'{cnt} {unit}s ago'
