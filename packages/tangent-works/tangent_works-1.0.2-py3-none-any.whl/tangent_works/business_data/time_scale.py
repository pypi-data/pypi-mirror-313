from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
import pandas as pd
import tangent_works.api.schemas as schemas
import tangent_works.api.schemas as schemas


class AggregationType(Enum):
    MEAN = "mean"
    MAX = "maximum"
    MIN = "minimum"
    SUM = "sum"
    MODE = "mode"


class TimeScaleBaseUnit(Enum):
    SECOND = "second"
    MINUTE = "minute"
    HOUR = "hour"
    DAY = "day"
    MONTH = "month"


@dataclass
class TimeScaleConfiguration:
    time_scale: pd.offsets.DateOffset
    aggregations: dict[str, AggregationType]
    drop_empty_rows: bool = True

    @classmethod
    def validate_configuration(cls, configuration: dict):
        schemas.validate_schema(configuration, schemas.time_scale_schema)

    @classmethod
    def from_dict(cls, conf: dict, time_series: TimeSeries):
        cls.validate_configuration(conf)

        return cls(
            time_scale=cls._get_time_scale(conf),
            aggregations=cls._get_aggregation_types(conf, time_series),
            drop_empty_rows=conf.get('drop_empty_rows', True)
        )

    def to_dict(self) -> dict:
        return {
            'time_scale': {
                'base_unit': self.time_scale.name,
                'value': self.time_scale.n
            },
            'aggregations': {
                key: value.value for key, value in self.aggregations.items()
            },
            'drop_empty_rows': self.drop_empty_rows
        }

    @classmethod
    def _get_time_scale(cls, conf: dict):
        time_scale_conf = conf['time_scale']

        match time_scale_conf['base_unit']:
            case 'month': time_scale = pd.offsets.MonthBegin()
            case 'day': time_scale = pd.offsets.Day()
            case 'hour': time_scale = pd.offsets.Hour()
            case 'minute': time_scale = pd.offsets.Minute()
            case 'second': time_scale = pd.offsets.Second()
            case _: raise ValueError(f"Unsupported time scale base unit: {time_scale_conf['base_unit']}")

        time_scale *= time_scale_conf['value']

        return time_scale

    @classmethod
    def _get_aggregation_types(cls, conf: dict, time_series: TimeSeries):
        if 'aggregations' not in conf:
            return {}

        aggregation_types = {}

        if 'common' in conf['aggregations']:
            for column in time_series.columns:
                if column == time_series.timestamp or column in time_series.group_keys:
                    continue

                aggregation_types[column] = cls._parse_aggregation_type(conf['aggregations']['common'])

        if 'individual' in conf['aggregations']:
            for aggregation in conf['aggregations']['individual']:
                name, value = aggregation['column_name'], aggregation['value']

                aggregation_types[name] = cls._parse_aggregation_type(value)

        return aggregation_types

    @staticmethod
    def _parse_aggregation_type(value: str):
        match value:
            case 'mean': return AggregationType.MEAN
            case 'sum': return AggregationType.SUM
            case 'minimum': return AggregationType.MIN
            case 'maximum': return AggregationType.MAX
            case 'mode': return AggregationType.MODE
            case _: raise ValueError(f"Unsupported aggregation type: {value}")
