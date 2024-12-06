from abc import ABC
from enum import Enum
from datetime import time
from dataclasses import dataclass
import numpy as np
import pandas as pd

from tangent_works.business_data.sampling_period import SamplingPeriod
from tangent_works.utils.datetime_utils import parse_time
from tangent_works.utils.general_utils import is_list_of_elements

TOL = 1e-8  # numeric tolerance for comparison of two models


class ForecastingObjective(Enum):
    FORECASTING = "forecasting"
    NORMAL_BEHAVIOR = "normal_behavior"


@dataclass
class Part(ABC):
    type: str

    def __post_init__(self):
        assert isinstance(self.type, str)

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, data):
        return cls(**data)


@dataclass
class PartBeta(Part):
    value: float

    def __post_init__(self):
        assert isinstance(self.value, float)

    def __eq__(self, other):
        if not isinstance(other, PartBeta):
            return False

        return abs(self.value - other.value) < TOL


@dataclass
class PartIntercept(Part):
    value: float

    def __post_init__(self):
        assert isinstance(self.value, float)

    def __eq__(self, other):
        if not isinstance(other, PartIntercept):
            return False

        return abs(self.value - other.value) < TOL


@dataclass
class PartWeekrest(Part):
    day: int
    offset: int

    def __post_init__(self):
        assert isinstance(self.day, int)
        assert isinstance(self.offset, int)


@dataclass
class PartWeekday(Part):
    day: int
    offset: int

    def __post_init__(self):
        assert isinstance(self.day, int)
        assert isinstance(self.offset, int)


@dataclass
class PartTrend(Part):
    step: str

    def __post_init__(self):
        assert isinstance(self.step, str)


@dataclass
class PartSimpleMovingAverage(Part):
    predictor: str
    window: int
    offset: int

    def __post_init__(self):
        assert isinstance(self.predictor, str)
        assert isinstance(self.window, int)
        assert isinstance(self.offset, int)


@dataclass
class PartCosinus(Part):
    period: float
    unit: str

    def __post_init__(self):
        assert isinstance(self.period, float)
        assert isinstance(self.unit, str)


@dataclass
class PartSinus(Part):
    period: float
    unit: str

    def __post_init__(self):
        assert isinstance(self.period, float)
        assert isinstance(self.unit, str)


@dataclass
class PartOneHotEncoding(Part):
    predictor: str
    category: str
    offset: int

    def __post_init__(self):
        assert isinstance(self.predictor, str)
        assert isinstance(self.category, str)
        assert isinstance(self.offset, int)


@dataclass
class PartOffset(Part):
    predictor: str
    offset: int

    def __post_init__(self):
        assert isinstance(self.predictor, str)
        assert isinstance(self.offset, int)


@dataclass
class PartMonth(Part):
    month: int

    def __post_init__(self):
        assert isinstance(self.month, int)


@dataclass
class PartExponentialMovingAverage(Part):
    predictor: str
    window: int
    offset: int

    def __post_init__(self):
        assert isinstance(self.predictor, str)
        assert isinstance(self.window, int)
        assert isinstance(self.offset, int)


@dataclass
class PartIdentity(Part):
    predictor: str

    def __post_init__(self):
        assert isinstance(self.predictor, str)


@dataclass
class PartPiecewiseLinear(Part):
    predictor: str
    knot: float
    subtype: int
    offset: int

    def __post_init__(self):
        assert isinstance(self.predictor, str)
        assert isinstance(self.knot, float)
        assert isinstance(self.subtype, int)
        assert isinstance(self.offset, int)

    def __eq__(self, other):
        if not isinstance(other, PartPiecewiseLinear):
            return False

        return (self.predictor == other.predictor and
                abs(self.knot - other.knot) < TOL and
                self.subtype == other.subtype and
                self.offset == other.offset)


@dataclass
class PartPublicHolidays(Part):
    predictor: str
    offset: int

    def __post_init__(self):
        assert isinstance(self.predictor, str)
        assert isinstance(self.offset, int)


@dataclass
class PartFourier(Part):
    period: float
    cos_orders: list[float]
    cos_betas: list[float]
    sin_orders: list[float]
    sin_betas: list[float]

    def __post_init__(self):
        assert isinstance(self.period, float)
        assert is_list_of_elements(self.cos_orders, float)
        assert is_list_of_elements(self.cos_betas, float)
        assert is_list_of_elements(self.sin_orders, float)
        assert is_list_of_elements(self.sin_betas, float)

    def __eq__(self, other):
        if not isinstance(other, PartFourier):
            return False

        return (self.period == other.period and
                self.cos_orders == other.cos_orders and
                np.allclose(self.cos_betas, other.cos_betas, atol=TOL) and
                self.sin_orders == other.sin_orders and
                np.allclose(self.sin_betas, other.sin_betas, atol=TOL))


@dataclass
class Term():
    importance: float
    parts: list[Part]

    def __post_init__(self):
        assert isinstance(self.importance, float)
        assert is_list_of_elements(self.parts, Part)

    def to_dict(self):
        return {
            'importance': self.importance,
            'parts': [p.to_dict() for p in self.parts],
        }

    def __eq__(self, other):
        if not isinstance(other, Term):
            return False

        return (abs(self.importance - other.importance) < TOL and
                self.parts == other.parts)

    @classmethod
    def from_dict(cls, data):
        part_types = []
        for part in data['parts']:
            match part['type']:
                case 'time_offsets': part_types.append(PartOffset)
                case 'exponential_moving_average': part_types.append(PartExponentialMovingAverage)
                case 'simple_moving_average': part_types.append(PartSimpleMovingAverage)
                case 'day_of_week': part_types.append(PartWeekday)
                case 'rest_of_week': part_types.append(PartWeekrest)
                case 'sin': part_types.append(PartSinus)
                case 'cos': part_types.append(PartCosinus)
                case 'piecewise_linear': part_types.append(PartPiecewiseLinear)
                case 'fourier': part_types.append(PartFourier)
                case 'month': part_types.append(PartMonth)
                case 'trend': part_types.append(PartTrend)
                case 'identity': part_types.append(PartIdentity)
                case 'public_holidays': part_types.append(PartPublicHolidays)
                case 'one_hot_encoding': part_types.append(PartOneHotEncoding)
                case 'intercept': part_types.append(PartIntercept)
                case 'β': part_types.append(PartBeta)
                case _: raise ValueError(f"Unknown model part type {part['type']}")

        return cls(
            importance=data['importance'],
            parts=[part_types[i].from_dict(data['parts'][i]) for i in range(len(data['parts']))],
        )


@dataclass
class VariableOffsets():
    name: str
    data_from: int
    data_to: int

    def __post_init__(self):
        assert isinstance(self.name, str)
        assert isinstance(self.data_from, int)
        assert isinstance(self.data_to, int)

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, data):
        return cls(**data)


@dataclass
class CaseVariableOffsets():
    name: str
    data_to: int

    def __post_init__(self):
        assert isinstance(self.name, str)
        assert isinstance(self.data_to, int)

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, data):
        return cls(**data)


@dataclass
class Case():
    day_time: time | None
    variable_offsets: list[CaseVariableOffsets]

    def __post_init__(self):
        assert isinstance(self.day_time, time) or self.day_time is None
        assert is_list_of_elements(self.variable_offsets, CaseVariableOffsets)

    def to_dict(self):
        return {
            'day_time': str(self.day_time) if self.day_time is not None else None,
            'variable_offsets': [vo.to_dict() for vo in self.variable_offsets],
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            day_time=parse_time(data['day_time'], "%H:%M:%S") if data['day_time'] is not None else None,
            variable_offsets=[CaseVariableOffsets.from_dict(vo) for vo in data['variable_offsets']],
        )


@dataclass
class Model():
    index: int
    terms: list[Term]
    day_time: time | None
    variable_offsets: list[VariableOffsets]
    samples_ahead: list[int]
    prediction_intervals: list[float]
    last_target_timestamp: np.datetime64
    cases: list[Case]

    def __post_init__(self):
        assert isinstance(self.index, int)
        assert is_list_of_elements(self.terms, Term)
        assert isinstance(self.day_time, time) or self.day_time is None
        assert is_list_of_elements(self.variable_offsets, VariableOffsets)
        assert is_list_of_elements(self.samples_ahead, int)
        assert is_list_of_elements(self.prediction_intervals, float)
        assert isinstance(self.last_target_timestamp, np.datetime64)
        assert is_list_of_elements(self.cases, Case)

    def to_dict(self):
        return {
            'index': self.index,
            'terms': [term.to_dict() for term in self.terms],
            'day_time': str(self.day_time) if self.day_time is not None else None,
            'variable_offsets': [vo.to_dict() for vo in self.variable_offsets],
            'samples_ahead': self.samples_ahead,
            'prediction_intervals': self.prediction_intervals,
            'last_target_timestamp': np.datetime_as_string(self.last_target_timestamp, unit='s'),
            'cases': [c.to_dict() for c in self.cases],
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            index=data['index'],
            terms=[Term.from_dict(term) for term in data['terms']],
            day_time=parse_time(data['day_time'], "%H:%M:%S") if data['day_time'] is not None else None,
            variable_offsets=[VariableOffsets.from_dict(vo) for vo in data['variable_offsets']],
            samples_ahead=data['samples_ahead'],
            prediction_intervals=data['prediction_intervals'],
            last_target_timestamp=np.datetime64(data['last_target_timestamp']),
            cases=[Case.from_dict(c) for c in data['cases']],
        )


@dataclass
class VariableProperties():
    type: str
    name: str
    data_from: int
    importance: float
    min: float | None = None
    max: float | None = None

    def __post_init__(self):
        assert isinstance(self.type, str)
        assert isinstance(self.name, str)
        assert isinstance(self.data_from, int)
        assert isinstance(self.importance, float)
        assert isinstance(self.min, float) or self.min is None
        assert isinstance(self.max, float) or self.max is None

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def __eq__(self, other):
        if not isinstance(other, VariableProperties):
            return False

        return (self.type == other.type and
                self.name == other.name and
                self.data_from == other.data_from and
                abs(self.importance - other.importance) < TOL and
                self.min == other.min and
                self.max == other.max)


@dataclass
class RCAParameters():
    index: int
    ri: list[float]
    g: list[float]
    m: list[float]

    def __post_init__(self):
        assert isinstance(self.index, int)
        assert is_list_of_elements(self.ri, float)
        assert is_list_of_elements(self.g, float)
        assert is_list_of_elements(self.m, float)

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def __eq__(self, other):
        if not isinstance(other, RCAParameters):
            return False

        return (self.index == other.index and
                self.ri == other.ri and
                self.g == other.g and
                self.m == other.m)


@dataclass
class ModelZoo():
    sampling_period: SamplingPeriod
    average_training_length: float
    models: list[Model]
    rca_parameters: list[RCAParameters]
    difficulty: float
    target_name: str
    holiday_name: str
    group_keys: list[str]
    upper_boundary: float
    lower_boundary: float
    daily_cycle: bool
    confidence_level: int
    variable_properties: list[VariableProperties]

    def __post_init__(self):
        assert isinstance(self.sampling_period, SamplingPeriod)
        assert isinstance(self.average_training_length, float)
        assert is_list_of_elements(self.models, Model)
        assert is_list_of_elements(self.rca_parameters, RCAParameters)
        assert isinstance(self.difficulty, float)
        assert isinstance(self.target_name, str)
        assert isinstance(self.holiday_name, str)
        assert is_list_of_elements(self.group_keys, str)
        assert isinstance(self.upper_boundary, float)
        assert isinstance(self.lower_boundary, float)
        assert isinstance(self.daily_cycle, bool)
        assert isinstance(self.confidence_level, int)
        assert is_list_of_elements(self.variable_properties, VariableProperties)

    def to_dict(self):
        return {
            'sampling_period': self.sampling_period.to_string(),
            'average_training_length': self.average_training_length,
            'models': [model.to_dict() for model in self.models],
            'rca_parameters': [rca_params.to_dict() for rca_params in self.rca_parameters],
            'difficulty': self.difficulty,
            'target_name': self.target_name,
            'holiday_name': self.holiday_name,
            'group_keys': self.group_keys,
            'upper_boundary': self.upper_boundary,
            'lower_boundary': self.lower_boundary,
            'daily_cycle': self.daily_cycle,
            'confidence_level': self.confidence_level,
            'variable_properties': [vp.to_dict() for vp in self.variable_properties],
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            sampling_period=SamplingPeriod.from_string(data['sampling_period']),
            average_training_length=data['average_training_length'],
            models=[Model.from_dict(model) for model in data['models']],
            rca_parameters=[RCAParameters.from_dict(rca_params) for rca_params in data['rca_parameters']],
            difficulty=data['difficulty'],
            target_name=data['target_name'],
            holiday_name=data['holiday_name'],
            group_keys=data['group_keys'],
            upper_boundary=data['upper_boundary'],
            lower_boundary=data['lower_boundary'],
            daily_cycle=data['daily_cycle'],
            confidence_level=data['confidence_level'],
            variable_properties=[VariableProperties.from_dict(vp) for vp in data['variable_properties']],
        )

    def __eq__(self, other):
        if not isinstance(other, ModelZoo):
            return False

        return (self.sampling_period == other.sampling_period and
                self.average_training_length == other.average_training_length and
                self.models == other.models and
                self.rca_parameters == other.rca_parameters and
                abs(self.difficulty - other.difficulty) < TOL and
                self.target_name == other.target_name and
                self.holiday_name == other.holiday_name and
                self.group_keys == other.group_keys and
                abs(self.upper_boundary - other.upper_boundary) < TOL and
                abs(self.lower_boundary - other.lower_boundary) < TOL and
                self.daily_cycle == other.daily_cycle and
                self.confidence_level == other.confidence_level and
                self.variable_properties == other.variable_properties)


@dataclass
class ForecastingModel():
    type: ForecastingObjective
    version: str
    model_zoo: ModelZoo

    def __post_init__(self):
        assert isinstance(self.type, ForecastingObjective)
        assert isinstance(self.version, str)
        assert isinstance(self.model_zoo, ModelZoo)

    @property
    def is_normal_behavior_model(self):
        return self.type == ForecastingObjective.NORMAL_BEHAVIOR

    def to_dict(self):
        return {
            'type': self.type.value,
            'version': self.version,
            'model_zoo': self.model_zoo.to_dict(),
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            type=ForecastingObjective(data['type']),
            version=data['version'],
            model_zoo=ModelZoo.from_dict(data['model_zoo'])
        )
