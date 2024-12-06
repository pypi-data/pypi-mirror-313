from datetime import datetime
import pandas as pd

from tangent_works.business_data.sampling_period import SamplingPeriod


def parse_time(datetime_str, format):
    return datetime.strptime(datetime_str, format).time()


def _find_closest_divisor(x, n):
    return next(a for a in range(x, n + 1) if n % a == 0)


def floor_timestamp_to_period(timestamp: pd.Timestamp, period: SamplingPeriod):
    if period.is_monthly:
        n_all_months = (timestamp.year * 12 + timestamp.month) // period.value * period.value
        n_years = n_all_months // 12
        n_months = n_all_months % n_all_months + 1
        return pd.Timestamp(datetime(n_years, n_months, 1))
    else:
        return floor_non_monthly_timestamps(timestamp, pd.Timedelta(seconds=period.value))


def floor_non_monthly_timestamps(timestamp: pd.Timestamp, offset: pd.Timedelta | pd.offsets.DateOffset):
    assert isinstance(offset, pd.Timedelta) or (isinstance(offset, pd.offsets.DateOffset) and not isinstance(offset, pd.offsets.MonthBegin))
    if offset == pd.offsets.Day(7):
        return (timestamp - pd.to_timedelta(timestamp.dayofweek, unit='d')).floor(pd.offsets.Day())
    else:
        return timestamp.floor(offset)


def timestamps_diff_in_months(d1, d2) -> float:
    return float((d1.year - d2.year) * 12 + d1.month - d2.month)


def diff_month(timestamps: pd.Series):
    timestamps_shifted = timestamps.shift()
    return pd.Series([timestamps_diff_in_months(d1, d2) for d1, d2 in zip(timestamps, timestamps_shifted)])
