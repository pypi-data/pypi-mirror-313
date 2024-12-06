import warnings
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from abc import ABC, abstractmethod
import pandas as pd
from tangent_works.utils.general_utils import is_optional_isinstance, convert_str_to_enum, is_optional_list_of_elements

from tangent_works.business_data.time_scale import TimeScaleConfiguration
from tangent_works.business_data.imputation import ImputationConfiguration
from tangent_works.utils.exceptions import TangentValidationError, TangentWarning
import tangent_works.api.schemas as schemas
from tangent_works.business_data.time_series import TimeSeries


class TargetOffsets(Enum):
    CLOSE = "close"
    COMMON = "common"
    NONE = "none"
    COMBINED = "combined"


class PredictorOffsets(Enum):
    CLOSE = "close"
    COMMON = "common"


class Transformation(Enum):
    EXPONENTIAL_MOVING_AVERAGE = "exponential_moving_average"
    REST_OF_WEEK = "rest_of_week"
    PERIODIC = "periodic"
    INTERCEPT = "intercept"
    PIECEWISE_LINEAR = "piecewise_linear"
    TIME_OFFSETS = "time_offsets"
    POLYNOMIAL = "polynomial"
    IDENTITY = "identity"
    SIMPLE_MOVING_AVERAGE = "simple_moving_average"
    MONTH = "month"
    TREND = "trend"
    DAY_OF_WEEK = "day_of_week"
    FOURIER = "fourier"
    PUBLIC_HOLIDAYS = "public_holidays"
    ONE_HOT_ENCODING = "one_hot_encoding"


def _parse_data_alignment_from_dict(input_data_alignment):
    output_data_alignment = {}
    if input_data_alignment:
        for col_alignment in input_data_alignment:
            output_data_alignment[col_alignment['column_name']] = pd.to_datetime(col_alignment['timestamp'])
    return output_data_alignment


def _default_horizon_unit():
    return {'base_unit': 'sample', 'value': 1}


class BuildConfiguration(ABC):
    @abstractmethod
    def to_dict(self):
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data):
        pass


@dataclass
class ForecastingBuildConfiguration(BuildConfiguration):
    prediction_from: dict = field(default_factory=_default_horizon_unit)
    prediction_to: dict = field(default_factory=_default_horizon_unit)
    target_offsets: Optional[TargetOffsets] = None
    predictor_offsets: PredictorOffsets = PredictorOffsets.COMMON
    allow_offsets: bool = True
    offset_limit: Optional[int] = None
    normalization: bool = True
    max_feature_count: Optional[int] = None
    transformations: Optional[list[Transformation]] = None
    daily_cycle: Optional[bool] = None
    confidence_level: int = 90
    target_column: Optional[str] = None
    holiday_column: str = ''
    categorical_columns: Optional[list[str]] = None
    data_alignment: dict = field(default_factory=dict)

    def __post_init__(self):
        assert isinstance(self.prediction_from, dict)
        assert isinstance(self.prediction_to, dict)
        assert is_optional_isinstance(self.target_offsets, TargetOffsets)
        assert isinstance(self.predictor_offsets, PredictorOffsets)
        assert isinstance(self.allow_offsets, bool)
        assert is_optional_isinstance(self.offset_limit, int)
        assert isinstance(self.normalization, bool)
        assert is_optional_isinstance(self.max_feature_count, int)
        assert is_optional_list_of_elements(self.transformations, Transformation)
        assert is_optional_isinstance(self.daily_cycle, bool)
        assert isinstance(self.confidence_level, int)
        assert is_optional_isinstance(self.target_column, str)
        assert isinstance(self.holiday_column, str)
        assert is_optional_list_of_elements(self.categorical_columns, str)
        assert isinstance(self.data_alignment, dict)

    def _convert_value(self, input_value):
        if isinstance(input_value, Enum):
            return input_value.value
        elif isinstance(input_value, list) and input_value and isinstance(input_value[0], Enum):
            return [item.value for item in input_value]
        else:
            return input_value

    def to_dict(self):
        return {
            key: self._convert_value(value)
            for key, value in self.__dict__.items()
            if value is not None
        }

    @classmethod
    def from_dict(cls, data, do_schema_validation: Optional[bool] = True):
        cls.validate_configuration(data, do_schema_validation)

        return cls(
            prediction_from=data.get('prediction_from', _default_horizon_unit()),
            prediction_to=data.get('prediction_to', _default_horizon_unit()),
            target_offsets=convert_str_to_enum(TargetOffsets, data.get('target_offsets')) if data.get('target_offsets') else cls.target_offsets,
            predictor_offsets=convert_str_to_enum(PredictorOffsets, data.get('predictor_offsets')) if data.get('predictor_offsets') else cls.predictor_offsets,
            allow_offsets=data.get('allow_offsets', cls.allow_offsets),
            offset_limit=data.get('offset_limit', cls.offset_limit),
            normalization=data.get('normalization', cls.normalization),
            max_feature_count=data.get('max_feature_count', cls.max_feature_count),
            transformations=[convert_str_to_enum(Transformation, f) for f in data.get('transformations')] if data.get('transformations') else cls.transformations,
            daily_cycle=data.get('daily_cycle', cls.daily_cycle),
            confidence_level=data.get('confidence_level', cls.confidence_level),
            target_column=data.get('target_column', cls.target_column),
            holiday_column=data.get('holiday_column', cls.holiday_column),
            categorical_columns=data.get('categorical_columns', cls.categorical_columns),
            data_alignment=_parse_data_alignment_from_dict(data.get('data_alignment'))
        )

    @classmethod
    def validate_configuration(cls, configuration: dict, do_schema_validation: Optional[bool] = True):
        if do_schema_validation:
            schemas.validate_schema(configuration, schemas.forecasting_build_model_schema)


@dataclass
class NormalBehaviorBuildConfiguration(BuildConfiguration):
    _forecasting_configuration = ForecastingBuildConfiguration

    def __init__(self,
                 target_offsets: Optional[TargetOffsets] = None,
                 allow_offsets: bool = True,
                 offset_limit: Optional[int] = None,
                 normalization: bool = True,
                 max_feature_count: Optional[int] = None,
                 transformations: Optional[list[Transformation]] = None,
                 daily_cycle: Optional[bool] = None,
                 confidence_level: float = 90,
                 target_column: Optional[str] = None,
                 holiday_column: str = '',
                 categorical_columns: Optional[list[str]] = None,
                 data_alignment: dict = None
                 ):

        self._forecasting_configuration = ForecastingBuildConfiguration(
            prediction_from={'base_unit': 'sample', 'value': 0},
            prediction_to={'base_unit': 'sample', 'value': 0},
            target_offsets=target_offsets,
            predictor_offsets=PredictorOffsets.COMMON,
            allow_offsets=allow_offsets,
            offset_limit=offset_limit,
            normalization=normalization,
            max_feature_count=max_feature_count,
            transformations=transformations,
            daily_cycle=daily_cycle,
            confidence_level=confidence_level,
            target_column=target_column,
            holiday_column=holiday_column,
            categorical_columns=categorical_columns,
            data_alignment=data_alignment if data_alignment else {}
        )

    def __getattr__(self, name):
        # Delegate attribute access to the wrapped configuration object
        return getattr(self._forecasting_configuration, name)

    def __setattr__(self, name, value):
        if name == '_forecasting_configuration':
            object.__setattr__(self, name, value)
        else:
            # Delegate attribute setting to the wrapped configuration object
            setattr(self._forecasting_configuration, name, value)

    def to_dict(self):
        return self._forecasting_configuration.to_dict()

    @classmethod
    def from_dict(cls, data):
        cls.validate_configuration(data)

        return cls(
            target_offsets=convert_str_to_enum(TargetOffsets, data.get('target_offsets')) if data.get('target_offsets') else cls._forecasting_configuration.target_offsets,
            allow_offsets=data.get('allow_offsets', cls._forecasting_configuration.allow_offsets),
            offset_limit=data.get('offset_limit', cls._forecasting_configuration.offset_limit),
            normalization=data.get('normalization', cls._forecasting_configuration.normalization),
            max_feature_count=data.get('max_feature_count', cls._forecasting_configuration.max_feature_count),
            transformations=[convert_str_to_enum(Transformation, f) for f in data.get('transformations')] if data.get('transformations') else cls._forecasting_configuration.transformations,
            daily_cycle=data.get('daily_cycle', cls._forecasting_configuration.daily_cycle),
            confidence_level=data.get('confidence_level', cls._forecasting_configuration.confidence_level),
            target_column=data.get('target_column', cls._forecasting_configuration.target_column),
            holiday_column=data.get('holiday_column', cls._forecasting_configuration.holiday_column),
            categorical_columns=data.get('categorical_columns', cls._forecasting_configuration.categorical_columns),
            data_alignment=_parse_data_alignment_from_dict(data.get('data_alignment'))
        )

    @classmethod
    def validate_configuration(cls, configuration: dict):
        schemas.validate_schema(configuration, schemas.forecasting_build_normal_behavior_model_schema)


@dataclass
class ForecastingPredictConfiguration:
    prediction_from: dict = field(default_factory=_default_horizon_unit)
    prediction_to: dict = field(default_factory=_default_horizon_unit)
    prediction_boundaries: Optional[dict] = None
    data_alignment: dict = field(default_factory=dict)

    def to_dict(self):
        return {
            key: value
            for key, value in self.__dict__.items()
            if value is not None
        }

    @classmethod
    def from_dict(cls, data, do_schema_validation: Optional[bool] = True):
        cls.validate_configuration(data, do_schema_validation)

        return cls(
            prediction_from=data.get('prediction_from', _default_horizon_unit()),
            prediction_to=data.get('prediction_to', _default_horizon_unit()),
            prediction_boundaries=data.get('prediction_boundaries', cls.prediction_boundaries),
            data_alignment=_parse_data_alignment_from_dict(data.get('data_alignment'))
        )

    @classmethod
    def validate_configuration(cls, configuration: dict, do_schema_validation: Optional[bool] = True):
        if do_schema_validation:
            schemas.validate_schema(configuration, schemas.forecasting_predict_schema)


@dataclass
class ForecastingRCAConfiguration:
    model_indexes: list = field(default_factory=_default_horizon_unit)

    @classmethod
    def from_dict(cls, data):
        cls.validate_configuration(data)

        return cls(
            model_indexes=data.get('model_indexes', [])
        )

    def to_dict(self):
        return {
            key: value
            for key, value in self.__dict__.items()
            if value is not None
        }

    @classmethod
    def validate_configuration(cls, configuration: dict):
        schemas.validate_schema(configuration, schemas.forecasting_rca_schema)


@dataclass
class AutoForecastingConfiguration:
    training_rows: Optional[list]
    prediction_rows: Optional[list]
    columns: Optional[list[str]]
    time_scale_configuration: Optional[TimeScaleConfiguration]
    imputation_by_column: Optional[dict]
    build_configuration: ForecastingBuildConfiguration
    predict_configuration: ForecastingPredictConfiguration

    @classmethod
    def from_dict(cls, data: dict, time_series: TimeSeries):
        cls.validate_configuration(data, time_series)

        preprocessing_conf = data.get('preprocessing', {})
        engine_conf = data.get('engine', {})

        columns = preprocessing_conf.get('columns')
        time_scale_configuration = TimeScaleConfiguration.from_dict(preprocessing_conf['time_scaling'], time_series) if 'time_scaling' in preprocessing_conf else None
        imputation_by_column = ImputationConfiguration.from_dict(preprocessing_conf['imputation'], time_series) if 'imputation' in preprocessing_conf else None
        if columns:
            if imputation_by_column:
                imputation_by_column = {column: value for column, value in imputation_by_column.items() if column in columns}
            if time_scale_configuration:
                time_scale_configuration.aggregations = {column: value for column, value in time_scale_configuration.aggregations.items() if column in columns}

        return cls(
            training_rows=cls._convert_rows(preprocessing_conf.get('training_rows'), 'training_rows'),
            prediction_rows=cls._convert_rows(preprocessing_conf.get('prediction_rows', []), 'prediction_rows'),
            columns=columns,
            time_scale_configuration=time_scale_configuration,
            imputation_by_column=imputation_by_column,
            build_configuration=ForecastingBuildConfiguration.from_dict(engine_conf, do_schema_validation=False),
            predict_configuration=ForecastingPredictConfiguration.from_dict(engine_conf, do_schema_validation=False),
        )

    def _convert_value(self, input_value):
        if isinstance(input_value, ForecastingBuildConfiguration):
            return input_value.to_dict()
        elif isinstance(input_value, ForecastingPredictConfiguration):
            return input_value.to_dict()
        elif isinstance(input_value, TimeScaleConfiguration):
            return input_value.to_dict()
        else:
            return input_value

    def to_dict(self) -> dict:
        return {
            key: self._convert_value(value)
            for key, value in self.__dict__.items()
            if value is not None
        }

    @ classmethod
    def _convert_rows(cls, rows, rows_name='rows'):
        if rows is None:
            return None
        try:
            rows = [(pd.to_datetime(row['from']), pd.to_datetime(row['to'])) for row in rows]
        except ValueError as e:
            raise TangentValidationError(f"Error converting {rows_name}: {e}") from e

        return cls._remove_time_zone_info(rows)

    @ staticmethod
    def _remove_time_zone_info(rows: list[tuple]):
        warn = False
        for i, row in enumerate(rows):
            if row[0].tz is not None or row[1].tz is not None:
                warn = True
                r0 = row[0].replace(tzinfo=None) if row[0].tz is not None else row[0]
                r1 = row[1].replace(tzinfo=None) if row[1].tz is not None else row[1]
                rows[i] = (r0, r1)
        if warn:
            warnings.warn("Timestamps in the rows configuration contains time-zone information, this will be ignored.", TangentWarning)
        return rows

    @ classmethod
    def validate_configuration(cls, configuration: dict, time_series: TimeSeries):
        schemas.validate_schema(configuration, schemas.auto_forecasting_schema)
        cls._validate_variable_columns(configuration, time_series.dataframe)

    @ staticmethod
    def _validate_variable_columns(configuration: dict, dataset: pd.DataFrame):
        columns = configuration.get('preprocessing', {}).get('columns', [])
        invalid_columns = set(columns) - set(dataset.columns)
        if invalid_columns:
            invalid_columns_str = ", ".join(invalid_columns)
            raise TangentValidationError(f"Invalid column names specified under 'columns': {invalid_columns_str}")
