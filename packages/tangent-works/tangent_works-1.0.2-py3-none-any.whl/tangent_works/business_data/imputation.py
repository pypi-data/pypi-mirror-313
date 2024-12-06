from __future__ import annotations
from enum import Enum
from dataclasses import dataclass
import tangent_works.api.schemas as schemas


class ImputationType(Enum):
    LINEAR = "linear"
    LOCF = "locf"


@dataclass
class Imputation():
    type: ImputationType
    max_gap: int


@dataclass
class ImputationConfiguration():
    @classmethod
    def validate_configuration(cls, configuration: dict):
        schemas.validate_schema(configuration, schemas.imputation_schema)

    @classmethod
    def from_dict(cls, conf: dict, time_series: TimeSeries):
        cls.validate_configuration(conf)

        imputation_by_column = {}

        if 'common' in conf:
            for column in time_series.columns:
                if column == time_series.timestamp or column in time_series.group_keys:
                    continue

                imputation_by_column[column] = Imputation(
                    type=cls._parse_imputation_type(conf['common']['type']),
                    max_gap=conf['common']['max_gap_length']
                )

        if 'individual' in conf:
            for individual in conf['individual']:
                column_name, imputation = individual['column_name'], individual['value']
                imputation_by_column[column_name] = Imputation(
                    type=cls._parse_imputation_type(imputation['type']),
                    max_gap=imputation['max_gap_length']
                )

        return imputation_by_column

    @staticmethod
    def _parse_imputation_type(value: str):
        match value:
            case 'linear': return ImputationType.LINEAR
            case 'locf': return ImputationType.LOCF
            case _: raise ValueError(f"Unsupported imputation type: {value}")
