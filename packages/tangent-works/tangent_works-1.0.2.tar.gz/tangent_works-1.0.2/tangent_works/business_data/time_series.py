from __future__ import annotations
import warnings
import pandas as pd
import numpy as np
from tangent_works.business_data.imputation import Imputation, ImputationConfiguration
from tangent_works.business_data.sampling_period import PeriodSeconds, PeriodMonths, SamplingPeriod
from tangent_works.business_data.time_scale import TimeScaleConfiguration
from tangent_works.business_logic.imputation import Imputer
from tangent_works.business_logic.time_scaling import TimeScaler
from tangent_works.utils.exceptions import TangentValidationError, TangentWarning
from tangent_works.utils.datetime_utils import diff_month


class TimeSeries:
    """
    A class used to represent a time series dataset.

    Attributes
    ----------
    timestamps : pd.Series
        Series of timestamps in the dataset.
    columns : pd.Index
        List of column names in the dataset.
    sampling_period : SamplingPeriod, optional
        Sampling period of the dataset. If not provided, sampling period is detected automatically.

    Methods
    -------
    validate(inplace)
        Validates correctness of the dataset (column names and types, timestamps and data).
    validate_timestamps_alignment(inplace)
        Validates alignment of timestamps with respect to the sampling period.
    time_scaling(configuration)
        Resamples the dataset according to the provided configuration.
    imputation(configuration)
        Imputes missing values in the dataset according to the provided imputation configuration.
    """

    def __init__(self, data: pd.DataFrame, timestamp_column: str = None, group_key_columns: list[str] = None):
        """
        Parameters
        ----------
        data : pd.DataFrame
            DataFrame containing the time series data.
        timestamp_column : str, optional
            Name of the column containing timestamps. If not provided, timestamp column is detected automatically.
        group_key_columns : list[str], optional
            A list of the column names which splits the panel data into individual groups. If empty, dataset is considered as individual time series data.
        """

        self.group_keys = group_key_columns if group_key_columns else list()
        self.dataframe = data.copy(deep=True)

        self.timestamp = timestamp_column if timestamp_column else self._detect_timestamp_column()
        self.validate()

        self._sort_dataframe()
        self._cast_types()

        self._sampling_period = self._calculate_sampling_period()

    @property
    def timestamps(self) -> pd.Series:
        """
        Series of timestamps in the dataset.
        """

        return self.dataframe[self.timestamp]

    @property
    def columns(self) -> pd.Index:
        """
        List of column names in the dataset.
        """

        return self.dataframe.columns

    @property
    def sampling_period(self) -> SamplingPeriod | None:
        """
        Sampling period of the dataset.
        """
        return self._sampling_period

    def _detect_timestamp_column(self) -> str:
        for column in self.dataframe.columns:
            if pd.api.types.is_datetime64_any_dtype(self.dataframe[column]):
                return column

        raise TangentValidationError("Can't find timestamp column.")

    def validate(self, inplace: bool = True) -> None:
        """
        Validates correctness of the dataset (column names and types, timestamps and data).

        Parameters
        ----------
        inplace : bool, optional
            If True, the method returns None. If False, the method returns the TimeSeries object reference.

        Returns
        -------
        None or TimeSeries
            Returns None if inplace is True, otherwise returns the TimeSeries object reference.
        """

        self._validate_column_names_and_types()
        self._validate_data()
        self._validate_timestamps()

        if not inplace:
            return self

    def time_scaling(self, configuration: dict) -> TimeSeries:
        """
        Resamples the dataset according to the provided configuration.

        Parameters
        ----------
        configuration : dict
            Configuration object containing the resampling parameters.

        Returns
        -------
        TimeSeries
            TimeSeries object with resampled data.
        """

        if configuration is None:
            return self

        time_scale_configuration = TimeScaleConfiguration.from_dict(configuration, self)
        scaled_data = TimeScaler().resample(self, time_scale_configuration)
        return TimeSeries(scaled_data, timestamp_column=self.timestamp, group_key_columns=self.group_keys)

    def imputation(self, configuration: dict) -> TimeSeries:
        """
        Imputes missing values in the dataset according to the provided imputation configuration.

        Parameters
        ----------
        configuration : dict
            Dictionary containing the imputation configuration for each column.

        Returns
        -------
        TimeSeries
            TimeSeries object with imputed data.
        """

        if configuration is None:
            return self

        imputation_configuration = ImputationConfiguration.from_dict(configuration, self)
        imputed_data = Imputer().impute(self, imputation_configuration)
        return TimeSeries(imputed_data, timestamp_column=self.timestamp, group_key_columns=self.group_keys)

    def _cast_types(self) -> None:
        numeric_columns = self.dataframe.select_dtypes(include='number').columns
        self.dataframe[numeric_columns] = self.dataframe[numeric_columns].astype(float)

        if self.timestamps.dt.tz is not None:
            self.dataframe[self.timestamp] = self.timestamps.apply(lambda x: x.replace(tzinfo=None))
            warnings.warn("Timestamps in the dataset contains time-zone, this information will be ignored.", TangentWarning)

    def _validate_column_names_and_types(self) -> None:
        if any(column_name == "" for column_name in self.columns):
            raise TangentValidationError("Column name cannot be empty.")

        duplicate_data_columns = self.columns[self.columns.duplicated()].tolist()
        if duplicate_data_columns:
            raise TangentValidationError(f"Dataframe column names must be unique. Duplicate column names: {duplicate_data_columns}. Ensure all names are unique.")

        user_columns_union = [self.timestamp] + self.group_keys

        for column in user_columns_union:
            if column not in self.columns:
                raise TangentValidationError(f"Column '{column}' not found in data.")

        if len(user_columns_union) != len(set(user_columns_union)):
            raise TangentValidationError("Specified column names must be unique.")

        if not pd.api.types.is_datetime64_any_dtype(self.timestamps):
            raise TangentValidationError("Timestamp column must be of datetime type.")

    def _validate_data(self) -> None:
        if self.dataframe[self.group_keys].isna().any().any():
            raise TangentValidationError("Group key column can not have missing values.")

        if self.dataframe.shape[1] <= len(self.group_keys) + 1:
            raise TangentValidationError("Time series data must contain a timestamp column, optionally group key columns, and at least one more column.")

    def _validate_timestamps(self) -> None:
        if self.timestamps.isna().any():
            raise TangentValidationError("Timestamp column can not have missing values.")

        if self.group_keys:
            grouped = self.dataframe.groupby(self.group_keys)
            for _, group in grouped:
                timestamps = group[self.timestamp]
                if timestamps.duplicated().any():
                    raise TangentValidationError("Timestamps must be unique for each combination of group keys.")

        else:
            if self.timestamps.duplicated().any():
                raise TangentValidationError("Timestamps must be unique.")

    def _sort_dataframe(self):
        if self.group_keys:
            self.dataframe = self.dataframe.groupby(self.group_keys).apply(lambda x: x.sort_values(by=self.timestamp)).reset_index(drop=True)

        else:
            if (self.timestamps.diff() < pd.Timedelta(0)).any():
                self.dataframe = self.dataframe.sort_values(self.timestamp).reset_index(drop=True)

    def _is_irregular_sampling_period(self, min_difference: pd.Timedelta) -> bool:
        if min_difference is None:
            return True

        elif min_difference < pd.Timedelta("1D"):
            if not self._is_whole_number(min_difference / pd.Timedelta("1s")):
                warnings.warn(f"Irregular sampling period - the minimum timestamp difference \"{min_difference.total_seconds()}s\" is not a whole number of seconds.", TangentWarning)
                return True
            if not self._is_whole_number(pd.Timedelta("1D") / min_difference):
                warnings.warn(f"Irregular sampling period - the minimum timestamp difference \"{min_difference}\" is not a divisor of one day period.", TangentWarning)
                return True

        elif min_difference < pd.Timedelta("28D"):
            if not self._is_whole_number(min_difference / pd.Timedelta("1D")):
                warnings.warn(f"Irregular sampling period - the minimum timestamp difference \"{min_difference}\" is not divisible by day period.", TangentWarning)
                return True

        irregular = self._timestamps_irregularly_spaced(min_difference)

        if irregular:
            warnings.warn("Irregular sampling period - timestamps do not conform to any sampling period.")

        return irregular

    def _timestamps_irregularly_spaced(self, min_difference: pd.Timedelta) -> bool:
        if min_difference < pd.Timedelta("28D"):
            timestamp_differences = self.timestamps.sort_values().diff()[1:]
            counts_of_occurence = timestamp_differences / min_difference

            return not all(self._is_whole_number(cnt) for cnt in counts_of_occurence)
        elif min_difference < pd.Timedelta("365D"):
            timestamp_differences = diff_month(self.timestamps)[1:]
            min_difference_rounded = round(min_difference / pd.Timedelta("30D"))
            counts_of_occurence = timestamp_differences / min_difference_rounded

            return not all(self._is_whole_number(cnt) for cnt in counts_of_occurence)
        else:
            timestamp_differences = self.timestamps.sort_values().diff()[1:]
            min_difference_rounded = round(min_difference / pd.Timedelta("365D")) * pd.Timedelta("365D")
            timestamp_differences_rounded = round(timestamp_differences / pd.Timedelta("365D")) * pd.Timedelta("365D")
            counts_of_occurence = timestamp_differences_rounded / min_difference_rounded

            return not all(self._is_whole_number(cnt) for cnt in counts_of_occurence)

    def validate_timestamps_alignment(self, inplace: bool = True) -> None:
        """
        Validates alignment of timestamps with respect to the sampling period.

        Parameters
        ----------
        inplace : bool, optional
            If True, the method returns None. If False, the method returns the TimeSeries object reference.

        Returns
        -------
        None or TimeSeries
            Returns None if inplace is True, otherwise returns the TimeSeries object reference.
        """

        min_difference = self._get_minimum_timestamp_difference()
        if min_difference < pd.Timedelta("28D"):
            first_timestamp = self.timestamps.iloc[0]
            if not self._is_whole_number((first_timestamp - first_timestamp.floor("D")) / min_difference):
                raise TangentValidationError("For weekly, daily or more frequent sampling periods, timestamps must be aligned to the beginning of day.")

        elif min_difference < pd.Timedelta("365D"):
            if not all(timestamp.microsecond + timestamp.second + timestamp.minute + timestamp.hour == 0 and
                       timestamp.day == 1 for timestamp in self.timestamps):
                raise TangentValidationError("For monthly sampling periods, timestamps must be aligned to the beginning of month (yyyy-mm-01).")

        else:
            if not all(timestamp.microsecond + timestamp.second + timestamp.minute + timestamp.hour == 0 and
                       timestamp.day == 1 and timestamp.month == 1 for timestamp in self.timestamps):
                raise TangentValidationError("For yearly sampling periods, timestamps must be aligned to the beginning of year (yyyy-01-01).")

        if not inplace:
            return self

    @staticmethod
    def _is_whole_number(number) -> bool:
        return int(number) == number

    @staticmethod
    def _find_minimum_period(x: pd.Series) -> pd.Timedelta:
        return x.diff()[1:].unique().min()

    def _get_minimum_timestamp_difference(self) -> pd.Timedelta | None:
        if self.group_keys:
            grouped = self.dataframe.groupby(self.group_keys)

            min_periods = [self._find_minimum_period(group[self.timestamp]) for _, group in grouped]
            min_periods_filtered = [period for period in min_periods if period is not pd.NaT]
            min_period = min(min_periods_filtered) if min_periods_filtered else pd.NaT
        else:
            min_period = self._find_minimum_period(self.timestamps)

        return min_period if min_period is not pd.NaT else None

    def _calculate_sampling_period(self) -> SamplingPeriod | None:
        sp = self._get_minimum_timestamp_difference()

        if self._is_irregular_sampling_period(sp):
            return None

        if sp is None:
            return None
        elif sp >= pd.Timedelta("365d"):
            n = sp // pd.Timedelta("365d")
            return PeriodMonths(n*12)
        elif sp >= pd.Timedelta("28d"):
            n = sp // pd.Timedelta("28d")
            return PeriodMonths(n)
        elif sp >= pd.Timedelta("0s"):
            n = sp // pd.Timedelta("1s")
            return PeriodSeconds(n)
        else:
            return ValueError("Sampling period calculation failed.")


class UnivariateTimeSeries:
    def __init__(self, data: pd.DataFrame, timestamp_column: str = None, group_key_columns: list[str] = None):
        self._time_series = TimeSeries(data, timestamp_column=timestamp_column, group_key_columns=group_key_columns)

        self._validate()

    def _validate(self) -> None:
        if not self._has_only_one_value_column():
            raise TangentValidationError("Univariate time series can contain only one value column.")

    def _has_only_one_value_column(self) -> bool:
        return len(self.columns) - len(self.group_keys) - 1 == 1  # minus one for timestamp

    @property
    def timestamps(self) -> pd.Series:
        return self._time_series.timestamps

    @property
    def sampling_period(self) -> SamplingPeriod | None:
        return self._time_series.sampling_period

    @property
    def columns(self) -> pd.Index:
        return self._time_series.columns

    @property
    def timestamp(self) -> str:
        return self._time_series.timestamp

    @property
    def dataframe(self) -> pd.DataFrame:
        return self._time_series.dataframe

    @property
    def group_keys(self) -> list[str]:
        return self._time_series.group_keys

    @property
    def values(self) -> pd.Series:
        column_with_values = [col for col in self.columns if col != self.timestamp][0]
        return self._time_series.dataframe[column_with_values]

    def drop_rows_with_nan_values(self) -> 'UnivariateTimeSeries':
        return UnivariateTimeSeries(data=self.dataframe.dropna(how='any'), timestamp_column=self.timestamp, group_key_columns=self.group_keys)
