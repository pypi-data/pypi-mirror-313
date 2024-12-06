from __future__ import annotations
import pandas as pd
import numpy as np
from tangent_works.business_data.imputation import Imputation, ImputationType
from tangent_works.business_data.sampling_period import SamplingPeriod
from tangent_works.utils.exceptions import TangentValidationError
from tangent_works.utils.datetime_utils import diff_month


class Imputer:
    def _linear_interpolation(self, start_value, end_value, n_new_samples):
        v = np.linspace(start_value, end_value, int(n_new_samples) + 2)
        return v[1:-1]

    def _forward_fill(self, start_value, n_new_samples):
        return np.full(n_new_samples, start_value)

    def _impute_gap(self, start_value, end_value, n_new_samples, imputation_type: ImputationType):
        match imputation_type:
            case ImputationType.LINEAR:
                return self._linear_interpolation(start_value, end_value, n_new_samples)
            case ImputationType.LOCF:
                return self._forward_fill(start_value, n_new_samples)
            case _:
                raise ValueError(f"Unsupported imputation: {imputation_type.value}")

    def _calculate_number_of_missing_rows(self, timestamps, sampling_period: SamplingPeriod):
        if sampling_period.is_monthly:
            missing_rows_counts = pd.Index(diff_month(pd.Series(timestamps))) / sampling_period.value - 1
        else:
            missing_rows_counts = timestamps.diff().total_seconds() / sampling_period.value - 1
        return missing_rows_counts

    @staticmethod
    def _get_default_imputation():
        return Imputation(type=ImputationType.LINEAR, max_gap=0)

    def _validate_before_impute(self, time_series: TimeSeries, imputation_by_column: dict[str, Imputation]):
        if time_series.dataframe.shape[0] < 2:
            raise TangentValidationError("There must be at least two rows in the dataset for imputation")
        if time_series.sampling_period is None:
            raise TangentValidationError("Datasets with irregular sampling periods cannot be imputed")
        for column_name in imputation_by_column:
            if column_name == time_series.timestamp:
                raise TangentValidationError(f"Invalid imputation column name: '{column_name}' is the timestamp column")

            if column_name not in time_series.columns:
                raise TangentValidationError(f"Invalid imputation column name: '{column_name}' not found in time series")

    def impute(self, time_series: TimeSeries, imputation_by_column: dict[str, Imputation]) -> pd.DataFrame:
        time_series.dataframe.set_index(time_series.timestamp, inplace=True, drop=False)

        self._validate_before_impute(time_series, imputation_by_column)

        sampling_period = time_series.sampling_period
        to_impute_list = []

        for column in time_series.columns:
            if column == time_series.timestamp:
                continue

            timestamps, values = [], []

            imputation = imputation_by_column.get(column, self._get_default_imputation())

            index_filter = time_series.dataframe[time_series.dataframe[column].notnull()].index
            missing_rows_counts = self._calculate_number_of_missing_rows(index_filter, sampling_period)
            condition = np.logical_and(missing_rows_counts > 0, missing_rows_counts <= imputation.max_gap)
            missing_rows_counts = missing_rows_counts[condition].astype(int)
            index_filter = index_filter[condition]

            for i, interval_end in enumerate(index_filter):
                num_rows_to_insert = missing_rows_counts[i]
                interval_start = interval_end - sampling_period * (num_rows_to_insert + 1)

                start_value = time_series.dataframe[column].loc[interval_start]
                end_value = time_series.dataframe[column].loc[interval_end]
                values_i = self._impute_gap(start_value, end_value, num_rows_to_insert, imputation.type)
                values.extend(values_i)

                frequency = pd.DateOffset(months=sampling_period.value) if sampling_period.is_monthly else pd.DateOffset(seconds=sampling_period.value)
                timestamps_i = pd.date_range(start=interval_start + sampling_period, end=interval_end - sampling_period, freq=frequency)
                timestamps.extend(timestamps_i)

            column_values_to_impute = pd.DataFrame({column: values}, index=pd.Index(name=time_series.dataframe.index.name, data=timestamps))
            to_impute_list.append(column_values_to_impute)

        to_impute = pd.concat(to_impute_list, axis=1, copy=False)
        if to_impute.empty:
            result = time_series.dataframe
        else:
            result = time_series.dataframe.combine_first(to_impute)
            result.sort_index(inplace=True)
            result.drop(time_series.timestamp, axis=1, inplace=True)
            result.reset_index(inplace=True)
            result = result[time_series.columns]  # maintain column order

        time_series.dataframe.reset_index(inplace=True, drop=True)  # return time_series to original form
        return result
