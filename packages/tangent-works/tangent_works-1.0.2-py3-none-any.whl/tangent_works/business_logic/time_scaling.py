from __future__ import annotations
import numpy as np
import pandas as pd
from tangent_works.business_data.time_scale import TimeScaleConfiguration
from tangent_works.business_data.time_scale import AggregationType
from tangent_works.utils.datetime_utils import floor_non_monthly_timestamps
from tangent_works.utils.exceptions import TangentValidationError

# The following code uses data offsets to resample time series.
# Detailed documentation on the usage of data offsets can be found:
# https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#dateoffset-objects


class TimeScaler:

    def _mode(self, x):
        r = pd.Series.mode(x)
        return r[0] if len(r) > 0 else np.nan

    def _get_aggregation_function(self, aggregation_type: AggregationType):
        match aggregation_type:
            case AggregationType.MEAN: return 'mean'
            case AggregationType.MIN: return 'min'
            case AggregationType.MAX: return 'max'
            case AggregationType.SUM: return 'sum'
            case AggregationType.MODE: return self._mode

    def _get_default_aggregation_type(self, time_series_column: pd.Series):
        if pd.api.types.is_numeric_dtype(time_series_column):
            return AggregationType.MEAN
        else:
            return AggregationType.MODE

    def _validate_before_resample(self, time_series: TimeSeries, aggregations: dict):
        for col, aggregation_type in aggregations.items():
            if col not in time_series.columns:
                raise TangentValidationError(f"Invalid aggregation column name: '{col}' not found in time series")

            if col == time_series.timestamp:
                raise TangentValidationError(f"Invalid aggregation column name: '{col}' is the timestamp column")

            if (not pd.api.types.is_numeric_dtype(time_series.dataframe[col])) and aggregation_type != AggregationType.MODE:
                raise TangentValidationError(f"Aggregation type '{aggregation_type.value}' is not allowed for non-numeric column '{col}'")

    def _get_prepared_dataframe(self, time_series: TimeSeries, time_scale: pd.offsets.DateOffset):
        output_dataframe = time_series.dataframe

        if not isinstance(time_scale, pd.offsets.MonthBegin) and time_scale > pd.offsets.Day(1):
            output_dataframe = output_dataframe.copy()
            output_dataframe[time_series.timestamp] = [floor_non_monthly_timestamps(t, time_scale) for t in output_dataframe[time_series.timestamp]]

        if time_series.group_keys:
            output_dataframe = output_dataframe.groupby(time_series.group_keys)

        return output_dataframe

    def resample(self, time_series: TimeSeries, config: TimeScaleConfiguration) -> pd.DataFrame:
        self._validate_before_resample(time_series, config.aggregations)

        for col in time_series.columns:
            if col not in config.aggregations and col != time_series.timestamp and col not in time_series.group_keys:
                config.aggregations[col] = self._get_default_aggregation_type(time_series.dataframe.loc[:, col])

        aggregation_functions = {col: self._get_aggregation_function(agg_type)
                                 for col, agg_type in config.aggregations.items()}

        scaled = self._get_prepared_dataframe(time_series, config.time_scale).resample(config.time_scale, closed='left', on=time_series.timestamp).agg(aggregation_functions)

        if config.drop_empty_rows:
            scaled = scaled.dropna(how='all')

        scaled.reset_index(inplace=True)
        return scaled[time_series.columns]  # maintain column order (pandas changes it during resampling)
