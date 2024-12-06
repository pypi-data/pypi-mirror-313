from dataclasses import dataclass, field

from tangent_works.business_data.forecasting_configuration import NormalBehaviorBuildConfiguration
from tangent_works.business_logic.anomaly_detection_transformations import (
    ResidualsTransformation,
    ResidualsIdentityTransformation,
    MovingAverageTransformation,
    get_residual_transformation_class_by_name,
)

from tangent_works.utils.exceptions import TangentValidationError
import tangent_works.api.schemas as schemas


@dataclass
class AutoSensitivity:
    min_value: float = 0.0
    max_value: float = 5.0

    def __post_init__(self):
        if self.min_value > self.max_value:
            raise TangentValidationError("min_value sensitivity bound can't be higher than max_value")

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            min_value=data['min_value'] if 'min_value' in data else cls.min_value,
            max_value=data['max_value'] if 'max_value' in data else cls.max_value
        )

    def to_dict(self) -> dict:
        return {
            'min_value': self.min_value,
            'max_value': self.max_value
        }


@dataclass
class DetectionLayerConfiguration:
    residuals_transformation: ResidualsTransformation
    sensitivity: float | AutoSensitivity = field(default_factory=AutoSensitivity)

    @classmethod
    def from_dict(cls, data: dict):
        transformation_class = get_residual_transformation_class_by_name(data['residuals_transformation']['type'])
        transformation = transformation_class.from_dict(data['residuals_transformation'])

        sensitivity = data['sensitivity'] if 'sensitivity' in data else AutoSensitivity()
        if isinstance(sensitivity, dict):
            sensitivity = AutoSensitivity.from_dict(sensitivity)

        return cls(
            residuals_transformation=transformation,
            sensitivity=sensitivity,
        )

    def to_dict(self) -> dict:
        return {
            'residuals_transformation': self.residuals_transformation.to_dict(),
            'sensitivity': self.sensitivity.to_dict() if isinstance(self.sensitivity, AutoSensitivity) else self.sensitivity
        }


@dataclass
class AnomalyDetectionBuildConfiguration:
    normal_behavior_configuration: NormalBehaviorBuildConfiguration
    detection_layers_configuration: list[DetectionLayerConfiguration]

    @classmethod
    def from_dict(cls, data: dict):
        cls.validate_configuration(data)

        if 'detection_layers' not in data or not data['detection_layers']:
            detection_layers_configuration = [
                DetectionLayerConfiguration(residuals_transformation=ResidualsIdentityTransformation()),
                DetectionLayerConfiguration(residuals_transformation=MovingAverageTransformation())
            ]
        else:
            detection_layers_configuration = [DetectionLayerConfiguration.from_dict(layer) for layer in data['detection_layers']]

        normal_behavior_configuration = data.get('normal_behavior', {})

        return cls(
            normal_behavior_configuration=NormalBehaviorBuildConfiguration.from_dict(normal_behavior_configuration),
            detection_layers_configuration=detection_layers_configuration
        )

    @classmethod
    def validate_configuration(cls, configuration: dict):
        schemas.validate_schema(configuration, schemas.anomaly_detection_build_model_schema)

    def to_dict(self) -> dict:
        return {
            'normal_behavior': self.normal_behavior_configuration.to_dict(),
            'detection_layers': [layer.to_dict() for layer in self.detection_layers_configuration]
        }
