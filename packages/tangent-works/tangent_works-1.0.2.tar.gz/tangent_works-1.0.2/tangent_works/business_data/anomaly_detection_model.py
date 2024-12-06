from dataclasses import dataclass, field
import numpy as np
from typing import Optional
from tangent_works.business_data.anomaly_detection_configuration import AutoSensitivity
from tangent_works.business_data.forecasting_model import ForecastingModel
from tangent_works.business_logic.anomaly_detection_transformations import (
    ResidualsTransformation,
    get_residual_transformation_class_by_name
)
from tangent_works.utils.general_utils import is_list_of_elements


@dataclass
class DensityModel:
    n_components: int = field(init=False)
    means: list[float]
    standard_deviations: list[float]
    weights: list[float]

    def __post_init__(self):
        self.n_components = len(self.means)
        self.weights = [w / sum(self.weights) for w in self.weights]

        assert self.n_components == len(self.standard_deviations) == len(self.weights)

    def evaluate(self, samples: list[float]) -> list[float]:
        return list(map(self.evaluate_sample, samples))

    def evaluate_sample(self, sample: float) -> float:
        return sum([self._evaluate_sample_in_normal_distribution_density(sample, self.means[i], self.standard_deviations[i]) * self.weights[i]
                    for i in range(self.n_components)])

    def _evaluate_sample_in_normal_distribution_density(self, sample: float, mean: float, std: float) -> float:
        return (1.0 / (std * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((sample - mean) / std) ** 2)

    def to_dict(self) -> dict:
        return {
            'n_components': self.n_components,
            'means': self.means,
            'standard_deviations': self.standard_deviations,
            'weights': self.weights,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            means=data['means'],
            standard_deviations=data['standard_deviations'],
            weights=data['weights']
        )


@dataclass
class AnomalyIndicatorParameters:
    translation: float
    threshold: float
    sensitivity: Optional[float | AutoSensitivity] = field(default_factory=AutoSensitivity(), init=True)

    def to_dict(self):
        return {
            'translation': self.translation,
            'threshold': self.threshold,
            'sensitivity': self.sensitivity.to_dict() if isinstance(self.sensitivity, AutoSensitivity) else self.sensitivity
        }

    @classmethod
    def from_dict(cls, data):
        if isinstance(data['sensitivity'], (float, AutoSensitivity)):
            sensitivity = data['sensitivity']
        elif isinstance(data['sensitivity'], dict):
            sensitivity = AutoSensitivity.from_dict(data['sensitivity'])
        else:
            raise TypeError(f"data['sensitivity'] should be of type float, AutoSensitivity or dict but got {type(data['sensitivity'])}")

        return cls(
            translation=data['translation'],
            threshold=data['threshold'],
            sensitivity=sensitivity
        )


@dataclass
class DetectionLayerModel:
    residuals_transformation: ResidualsTransformation
    density_model: DensityModel
    anomaly_indicator_parameters: AnomalyIndicatorParameters

    def to_dict(self):
        return {
            'residuals_transformation': self.residuals_transformation.to_dict(),
            'density_model': self.density_model.to_dict(),
            'anomaly_indicator_parameters': self.anomaly_indicator_parameters.to_dict(),
        }

    @classmethod
    def from_dict(cls, data):
        transformation_class = get_residual_transformation_class_by_name(data['residuals_transformation']['type'])
        transformation = transformation_class.from_dict(data['residuals_transformation'])

        return cls(
            residuals_transformation=transformation,
            density_model=DensityModel.from_dict(data['density_model']),
            anomaly_indicator_parameters=AnomalyIndicatorParameters.from_dict(data['anomaly_indicator_parameters']),
        )


@dataclass
class AnomalyDetectionModel:
    type: str = field(default="anomaly_detection", init=False)
    version: str
    normal_behavior_model: ForecastingModel
    detection_layer_models: list[DetectionLayerModel]

    def __post_init__(self):
        assert isinstance(self.type, str)
        assert isinstance(self.version, str)
        assert isinstance(self.normal_behavior_model, ForecastingModel)
        assert is_list_of_elements(self.detection_layer_models, DetectionLayerModel)

    def to_dict(self):
        return {
            'type': self.type,
            'version': self.version,
            'normal_behavior_model': self.normal_behavior_model.to_dict(),
            'detection_layer_models': [model.to_dict() for model in self.detection_layer_models]
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            version=data['version'],
            normal_behavior_model=ForecastingModel.from_dict(data['normal_behavior_model']),
            detection_layer_models=[DetectionLayerModel.from_dict(model) for model in data['detection_layer_models']]
        )
