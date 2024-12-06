from abc import ABC, abstractmethod
import pandas as pd
import numpy as np
from tangent_works.business_data.time_series import UnivariateTimeSeries
from tangent_works.business_data.sampling_period import SamplingPeriod, PeriodSeconds
from tangent_works.utils.exceptions import TangentValidationError


class Auto():
    def __str__(self):
        return 'auto'


class ResidualsTransformation(ABC):
    def __init__(self, window_length: int | Auto = Auto()):
        self._window_length = window_length

    @property
    @abstractmethod
    def full_name(self) -> str:
        pass

    def apply(self, residuals: UnivariateTimeSeries) -> UnivariateTimeSeries:
        sampling_period = residuals.sampling_period

        if isinstance(self._window_length, Auto):
            self._set_default_window_length(sampling_period)

        if sampling_period.is_monthly:
            window = self._get_params_for_sampling_period_in_months(sampling_period)
        else:
            window = self._get_params_for_sampling_period_in_seconds(sampling_period)

        fn = self._get_function_to_apply()
        transformed = residuals.dataframe.rolling(on=residuals.timestamp, window=window, min_periods=self._window_length).apply(fn)

        return UnivariateTimeSeries(data=transformed, timestamp_column=residuals.timestamp)

    def _get_params_for_sampling_period_in_months(self, sampling_period: SamplingPeriod) -> tuple[pd.Timedelta, int]:
        days_in_month = 30.5
        sampling_period_in_days = days_in_month * sampling_period.value
        window_in_days = sampling_period_in_days * self._window_length - days_in_month / 2
        window_in_days = int(np.round(window_in_days))
        window = pd.Timedelta(days=window_in_days)
        return window

    def _get_params_for_sampling_period_in_seconds(self, sampling_period: SamplingPeriod) -> tuple[pd.Timedelta, int]:
        window = pd.Timedelta(seconds=sampling_period.value * self._window_length)
        return window

    @abstractmethod
    def _set_default_window_length(self, sampling_period: SamplingPeriod) -> None:
        pass

    @abstractmethod
    def _get_function_to_apply(self) -> callable:
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict) -> 'ResidualsTransformation':
        pass

    def __eq__(self, other):
        return type(self) == type(other)


class ResidualsIdentityTransformation(ResidualsTransformation):
    name = 'residuals'

    def __init__(self):
        super().__init__(window_length=1)

    @property
    def full_name(self) -> str:
        return self.name

    def _set_default_window_length(self, sampling_period: SamplingPeriod) -> None:
        self._window_length = 1

    def _get_function_to_apply(self) -> callable:
        return lambda x: x

    def to_dict(self) -> dict:
        return {
            'type': self.name
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'ResidualsIdentityTransformation':
        return ResidualsIdentityTransformation()


class ResidualsChangeTransformation(ResidualsTransformation):
    name = 'residuals_change'

    def __init__(self, window_length: int | Auto = Auto()):
        super().__init__(window_length=window_length)

    @ property
    def full_name(self) -> str:
        return f'{self.name}_{self._window_length}'

    def _set_default_window_length(self, sampling_period: SamplingPeriod) -> None:
        if sampling_period.is_monthly or sampling_period >= PeriodSeconds(60*60*24):
            self._window_length = 9
        else:
            if sampling_period > PeriodSeconds(60*10):
                self._window_length = 49
            else:
                self._window_length = 73

    def _get_function_to_apply(self) -> callable:
        def f(x):
            past = x.iloc[:-1]
            past_med = np.median(past)
            return (x.iloc[-1] - past_med) / (1 + np.sum(np.abs(past - past_med)))

        return f

    def to_dict(self) -> dict:
        return {
            'type': self.name
        }

    @ classmethod
    def from_dict(cls, data: dict) -> 'ResidualsChangeTransformation':
        window_length = data['window_length'] if 'window_length' in data else Auto()
        return ResidualsChangeTransformation(window_length=window_length)


class MovingAverageTransformation(ResidualsTransformation):
    name = 'moving_average'

    def __init__(self, window_length: int | Auto = Auto()):
        super().__init__(window_length=window_length)

    @property
    def full_name(self) -> str:
        return f'{self.name}_{self._window_length}'

    def _set_default_window_length(self, sampling_period: SamplingPeriod) -> None:
        if sampling_period.is_monthly or sampling_period >= PeriodSeconds(60*60*24):
            self._window_length = 9
        else:
            if sampling_period > PeriodSeconds(60*10):
                self._window_length = 24
            else:
                self._window_length = 36

    def _get_function_to_apply(self) -> callable:
        return np.mean

    def to_dict(self) -> dict:
        return {
            'type': self.name,
            'window_length': 'auto' if isinstance(self._window_length, Auto) else self._window_length
        }

    @ classmethod
    def from_dict(cls, data: dict) -> 'MovingAverageTransformation':
        window_length = data['window_length'] if 'window_length' in data else Auto()
        return MovingAverageTransformation(window_length=window_length)

    def __eq__(self, other):
        if isinstance(other, MovingAverageTransformation):
            return other._window_length == self._window_length
        return False


class MovingAverageChangeTransformation(ResidualsTransformation):
    name = 'moving_average_change'

    def __init__(self, window_lengths: list[int] | Auto = Auto()):
        if isinstance(window_lengths, list):
            if window_lengths[1] >= window_lengths[0]:
                raise TangentValidationError(f'Subwindow length must be less than window length in {self.name} transformation.')

        super().__init__(window_length=window_lengths[0] if not isinstance(window_lengths, Auto) else Auto())
        self._subwindow_length = window_lengths[1] if not isinstance(window_lengths, Auto) else 1

    @property
    def full_name(self) -> str:
        return f'{self.name}_{self._window_length}_{self._subwindow_length}'

    def _set_default_window_length(self, sampling_period: SamplingPeriod) -> None:
        if sampling_period.is_monthly or sampling_period >= PeriodSeconds(60*60*24):
            self._subwindow_length = 4
            self._window_length = 16
        else:
            if sampling_period > PeriodSeconds(60*10):
                self._subwindow_length = 12
                self._window_length = 60
            else:
                self._subwindow_length = 18
                self._window_length = 90

    def _get_function_to_apply(self) -> callable:
        def f(x):
            mean1 = np.mean(x.iloc[-self._subwindow_length:])
            mean2 = np.mean(x.iloc[:-self._subwindow_length])
            median1 = np.median(x.iloc[:-self._subwindow_length])
            return (mean1 - mean2) / (1 + np.sum(np.abs(x.iloc[:-self._subwindow_length] - median1)) / (self._window_length - self._subwindow_length))

        return f

    def to_dict(self) -> dict:
        return {
            'type': self.name,
            'window_length': 'auto' if isinstance(self._window_length, Auto) else self._window_length,
            'subwindow_length': 'auto' if isinstance(self._subwindow_length, Auto) else self._subwindow_length
        }

    @ classmethod
    def from_dict(cls, data: dict) -> 'MovingAverageChangeTransformation':
        window_lengths = data['window_lengths'] if 'window_lengths' in data else Auto()
        return MovingAverageChangeTransformation(window_lengths=window_lengths)

    def __eq__(self, other):
        if isinstance(other, MovingAverageChangeTransformation):
            return other._window_length == self._window_length and other._subwindow_length == self._subwindow_length
        return False


class StandardDeviationTransformation(ResidualsTransformation):
    name = 'standard_deviation'

    def __init__(self, window_length: int | Auto = Auto()):
        super().__init__(window_length=window_length)

    @property
    def full_name(self) -> str:
        return f'{self.name}_{self._window_length}'

    def _set_default_window_length(self, sampling_period: SamplingPeriod) -> None:
        if sampling_period.is_monthly or sampling_period >= PeriodSeconds(60*60*24):
            self._window_length = 9
        else:
            if sampling_period > PeriodSeconds(60*10):
                self._window_length = 24
            else:
                self._window_length = 36

    def _get_function_to_apply(self) -> callable:
        return np.std

    def to_dict(self) -> dict:
        return {
            'type': self.name,
            'window_length': 'auto' if isinstance(self._window_length, Auto) else self._window_length
        }

    @ classmethod
    def from_dict(cls, data: dict) -> 'StandardDeviationTransformation':
        window_length = data['window_length'] if 'window_length' in data else Auto()
        return StandardDeviationTransformation(window_length=window_length)

    def __eq__(self, other):
        if isinstance(other, StandardDeviationTransformation):
            return other._window_length == self._window_length
        return False


class StandardDeviationChangeTransformation(ResidualsTransformation):
    name = 'standard_deviation_change'

    def __init__(self, window_lengths: list[int] | Auto = Auto()):
        if isinstance(window_lengths, list):
            if window_lengths[1] >= window_lengths[0]:
                raise TangentValidationError(f'Subwindow length must be less than window length in {self.name} transformation.')

        super().__init__(window_length=window_lengths[0] if not isinstance(window_lengths, Auto) else Auto())
        self._subwindow_length = window_lengths[1] if not isinstance(window_lengths, Auto) else 1

    @property
    def full_name(self) -> str:
        return f'{self.name}_{self._window_length}_{self._subwindow_length}'

    def _set_default_window_length(self, sampling_period: SamplingPeriod) -> None:
        if sampling_period.is_monthly or sampling_period >= PeriodSeconds(60*60*24):
            self._subwindow_length = 4
            self._window_length = 16
        else:
            if sampling_period > PeriodSeconds(60*10):
                self._subwindow_length = 12
                self._window_length = 60
            else:
                self._subwindow_length = 18
                self._window_length = 90

    def _get_function_to_apply(self) -> callable:
        def f(x):
            mean1 = np.std(x.iloc[-self._subwindow_length:])
            mean2 = np.std(x.iloc[:-self._subwindow_length])
            median1 = np.median(x.iloc[:-self._subwindow_length])
            return (mean1 - mean2) / (1 + np.sum(np.abs(x.iloc[:-self._subwindow_length] - median1)) / (self._window_length - self._subwindow_length))

        return f

    def to_dict(self) -> dict:
        return {
            'type': self.name,
            'window_length': 'auto' if isinstance(self._window_length, Auto) else self._window_length,
            'subwindow_length': 'auto' if isinstance(self._subwindow_length, Auto) else self._subwindow_length
        }

    @ classmethod
    def from_dict(cls, data: dict) -> 'StandardDeviationChangeTransformation':
        window_lengths = data['window_lengths'] if 'window_lengths' in data else Auto()
        return StandardDeviationChangeTransformation(window_lengths=window_lengths)

    def __eq__(self, other):
        if isinstance(other, StandardDeviationChangeTransformation):
            return other._window_length == self._window_length and other._subwindow_length == self._subwindow_length
        return False


def get_residual_transformation_class_by_name(transformation_name: str):
    residual_transformation_classes = ResidualsTransformation.__subclasses__()

    for residual_transformation_class in residual_transformation_classes:
        if residual_transformation_class.name == transformation_name:
            return residual_transformation_class

    raise ValueError(f'{transformation_name} is not a valid residual transformation name')
