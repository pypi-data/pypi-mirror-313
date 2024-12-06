import os
import json
from jsonschema import validate, ValidationError
from tangent_works.utils.exceptions import TangentValidationError

SCHEMAS_JSON = r"""{
  "AutoForecastingConfiguration": {
    "title": "Auto-forecast configuration",
    "description": "Auto-forecast configuration",
    "type": "object",
    "additionalProperties": false,
    "properties": {
      "preprocessing": {
        "$ref": "#/definitions/AutoForecastingPreprocessingConfiguration"
      },
      "engine": {
        "$ref": "#/definitions/AutoForecastingEngineConfiguration"
      }
    }
  },
  "BuildConfiguration": {
    "title": "Build configuration",
    "description": "Build configuration",
    "type": "object",
    "additionalProperties": false,
    "properties": {
      "target_column": {
        "$ref": "#/definitions/TargetColumn"
      },
      "categorical_columns": {
        "$ref": "#/definitions/CategoricalColumns"
      },
      "holiday_column": {
        "$ref": "#/definitions/HolidayColumn"
      },
      "prediction_from": {
        "$ref": "#/definitions/PredictionFrom"
      },
      "prediction_to": {
        "$ref": "#/definitions/PredictionTo"
      },
      "target_offsets": {
        "$ref": "#/definitions/TargetOffsets"
      },
      "predictor_offsets": {
        "$ref": "#/definitions/PredictorOffsets"
      },
      "allow_offsets": {
        "$ref": "#/definitions/AllowOffsets"
      },
      "offset_limit": {
        "$ref": "#/definitions/OffsetLimit"
      },
      "normalization": {
        "$ref": "#/definitions/Normalization"
      },
      "max_feature_count": {
        "$ref": "#/definitions/MaxFeatureCount"
      },
      "transformations": {
        "$ref": "#/definitions/TransformationsForecasting"
      },
      "daily_cycle": {
        "$ref": "#/definitions/DailyCycle"
      },
      "confidence_level": {
        "$ref": "#/definitions/ConfidenceLevel"
      },
      "data_alignment": {
        "$ref": "#/definitions/DataAlignment"
      }
    }
  },
  "BuildNormalBehaviorConfiguration": {
    "title": "Normal behavior build configuration",
    "description": "Normal behavior build configuration",
    "type": "object",
    "additionalProperties": false,
    "properties": {
      "target_column": {
        "description": "Defines which column represents the target variable, identified by name. \nIf not specified, the first non-timestamp column will be taken.\n",
        "type": "string",
        "example": "y"
      },
      "holiday_column": {
        "description": "Defines which column represents the holiday column, identified by name.\nIf not set, no column is defined as holiday column.\n",
        "type": "string",
        "example": "PH"
      },
      "target_offsets": {
        "$ref": "#/definitions/TargetOffsetsForNormalBehavior"
      },
      "allow_offsets": {
        "$ref": "#/definitions/AllowOffsets"
      },
      "offset_limit": {
        "$ref": "#/definitions/OffsetLimit"
      },
      "normalization": {
        "$ref": "#/definitions/Normalization"
      },
      "max_feature_count": {
        "$ref": "#/definitions/MaxFeatureCount"
      },
      "transformations": {
        "$ref": "#/definitions/TransformationsForecasting"
      },
      "daily_cycle": {
        "$ref": "#/definitions/DailyCycle"
      },
      "confidence_level": {
        "$ref": "#/definitions/ConfidenceLevel"
      },
      "categorical_columns": {
        "$ref": "#/definitions/CategoricalColumns"
      },
      "data_alignment": {
        "$ref": "#/definitions/DataAlignment"
      }
    }
  },
  "BuildAnomalyDetectionConfiguration": {
    "title": "Anomaly detection build configuration",
    "description": "Anomaly detection build configuration",
    "type": "object",
    "additionalProperties": false,
    "properties": {
      "normal_behavior": {
        "$ref": "#/definitions/BuildNormalBehaviorConfiguration"
      },
      "detection_layers": {
        "type": "array",
        "minItems": 1,
        "items": {
          "type": "object",
          "additionalProperties": false,
          "properties": {
            "residuals_transformation": {
              "oneOf": [
                {
                  "$ref": "#/definitions/ResidualsIdentityTransformation"
                },
                {
                  "$ref": "#/definitions/ResidualsChangeTransformation"
                },
                {
                  "$ref": "#/definitions/MovingAverageTransformation"
                },
                {
                  "$ref": "#/definitions/MovingAverageChangeTransformation"
                },
                {
                  "$ref": "#/definitions/StandardDeviationTransformation"
                },
                {
                  "$ref": "#/definitions/StandardDeviationChangeTransformation"
                }
              ]
            },
            "sensitivity": {
              "oneOf": [
                {
                  "type": "number",
                  "format": "double",
                  "minimum": 0,
                  "maximum": 100
                },
                {
                  "type": "object",
                  "additionalProperties": false,
                  "properties": {
                    "min_value": {
                      "type": "number",
                      "format": "double",
                      "minimum": 0,
                      "maximum": 100
                    },
                    "max_value": {
                      "type": "number",
                      "format": "double",
                      "minimum": 0,
                      "maximum": 100
                    }
                  }
                }
              ]
            }
          }
        }
      }
    }
  },
  "PredictConfiguration": {
    "title": "Predict configuration",
    "description": "Predict configuration",
    "type": "object",
    "additionalProperties": false,
    "properties": {
      "prediction_from": {
        "$ref": "#/definitions/PredictionFrom"
      },
      "prediction_to": {
        "$ref": "#/definitions/PredictionTo"
      },
      "prediction_boundaries": {
        "$ref": "#/definitions/PredictionBoundaries"
      },
      "data_alignment": {
        "$ref": "#/definitions/DataAlignment"
      }
    }
  },
  "RCAConfiguration": {
    "title": "RCA configuration",
    "description": "RCA configuration",
    "type": "object",
    "additionalProperties": false,
    "properties": {
      "model_indexes": {
        "$ref": "#/definitions/ModelIndexes"
      }
    }
  },
  "AutoForecastingPreprocessingConfiguration": {
    "title": "Preprocessing configuration",
    "description": "Preprocessing configuration",
    "type": "object",
    "additionalProperties": false,
    "properties": {
      "training_rows": {
        "description": "Defines which samples should be used for model building.\nIf not set, all timestamps in the dataset will be used.\n",
        "type": "array",
        "items": {
          "$ref": "#/definitions/Range"
        },
        "minItems": 1
      },
      "prediction_rows": {
        "description": "Defines which samples should be forecasted. If not set, none will be used.\n",
        "type": "array",
        "items": {
          "$ref": "#/definitions/Range"
        },
        "minItems": 1
      },
      "columns": {
        "description": "Defines which samples should be forecasted. If not set, none will be used.\n",
        "type": "array",
        "items": {
          "type": "string"
        },
        "example": [
          "Target",
          "Predictor"
        ]
      },
      "imputation": {
        "$ref": "#/definitions/ImputeConfiguration"
      },
      "time_scaling": {
        "$ref": "#/definitions/TimeScaleConfiguration"
      }
    }
  },
  "AutoForecastingEngineConfiguration": {
    "title": "Engine configuration",
    "description": "Engine configuration",
    "type": "object",
    "additionalProperties": false,
    "properties": {
      "target_column": {
        "$ref": "#/definitions/TargetColumn"
      },
      "categorical_columns": {
        "$ref": "#/definitions/CategoricalColumns"
      },
      "holiday_column": {
        "$ref": "#/definitions/HolidayColumn"
      },
      "prediction_from": {
        "$ref": "#/definitions/PredictionFrom"
      },
      "prediction_to": {
        "$ref": "#/definitions/PredictionTo"
      },
      "target_offsets": {
        "$ref": "#/definitions/TargetOffsets"
      },
      "predictor_offsets": {
        "$ref": "#/definitions/PredictorOffsets"
      },
      "allow_offsets": {
        "$ref": "#/definitions/AllowOffsets"
      },
      "offset_limit": {
        "$ref": "#/definitions/OffsetLimit"
      },
      "normalization": {
        "$ref": "#/definitions/Normalization"
      },
      "max_feature_count": {
        "$ref": "#/definitions/MaxFeatureCount"
      },
      "transformations": {
        "$ref": "#/definitions/TransformationsForecasting"
      },
      "daily_cycle": {
        "$ref": "#/definitions/DailyCycle"
      },
      "confidence_level": {
        "$ref": "#/definitions/ConfidenceLevel"
      },
      "data_alignment": {
        "$ref": "#/definitions/DataAlignment"
      },
      "prediction_boundaries": {
        "$ref": "#/definitions/PredictionBoundaries"
      }
    }
  },
  "ResidualsIdentityTransformation": {
    "type": "object",
    "additionalProperties": false,
    "properties": {
      "type": {
        "type": "string",
        "enum": [
          "residuals"
        ]
      }
    }
  },
  "ResidualsChangeTransformation": {
    "type": "object",
    "additionalProperties": false,
    "properties": {
      "type": {
        "type": "string",
        "enum": [
          "residuals_change"
        ]
      },
      "window_length": {
        "type": "integer",
        "minimum": 2
      }
    }
  },
  "MovingAverageTransformation": {
    "type": "object",
    "additionalProperties": false,
    "properties": {
      "type": {
        "type": "string",
        "enum": [
          "moving_average"
        ]
      },
      "window_length": {
        "type": "integer",
        "minimum": 1
      }
    }
  },
  "MovingAverageChangeTransformation": {
    "type": "object",
    "additionalProperties": false,
    "properties": {
      "type": {
        "type": "string",
        "enum": [
          "moving_average_change"
        ]
      },
      "window_lengths": {
        "type": "array",
        "minItems": 2,
        "maxItems": 2,
        "items": {
          "type": "integer",
          "minimum": 1
        }
      }
    }
  },
  "StandardDeviationTransformation": {
    "type": "object",
    "additionalProperties": false,
    "properties": {
      "type": {
        "type": "string",
        "enum": [
          "standard_deviation"
        ]
      },
      "window_length": {
        "type": "integer",
        "minimum": 1
      }
    }
  },
  "StandardDeviationChangeTransformation": {
    "type": "object",
    "additionalProperties": false,
    "properties": {
      "type": {
        "type": "string",
        "enum": [
          "standard_deviation_change"
        ]
      },
      "window_lengths": {
        "type": "array",
        "minItems": 2,
        "maxItems": 2,
        "items": {
          "type": "integer",
          "minimum": 1
        }
      }
    }
  },
  "Aggregations": {
    "description": "The aggregation functions to use for columns.\nThe default aggregation is mean for numerical variables and mode for categorical variables.\n",
    "type": "object",
    "additionalProperties": false,
    "properties": {
      "common": {
        "$ref": "#/definitions/AggregationFunction",
        "description": "The aggregation function to use for all columns except those specified in the individual array"
      },
      "individual": {
        "type": "array",
        "uniqueItems": true,
        "minItems": 1,
        "items": {
          "type": "object",
          "additionalProperties": false,
          "properties": {
            "column_name": {
              "type": "string",
              "example": "Predictor"
            },
            "value": {
              "$ref": "#/definitions/AggregationFunction"
            }
          }
        }
      }
    }
  },
  "AggregationFunction": {
    "description": "The aggregation function to use for a dataset column.\n",
    "type": "string",
    "enum": [
      "mean",
      "sum",
      "minimum",
      "maximum",
      "mode"
    ]
  },
  "CategoricalColumns": {
    "description": "Defines which columns represents the categorical columns, identified by name.\n",
    "type": "array",
    "uniqueItems": true,
    "minItems": 1,
    "items": {
      "type": "string"
    },
    "example": [
      "Category",
      "Status"
    ],
    "default": []
  },
  "TargetColumn": {
    "description": "Defines which column represents the target variable, identified by name. \nIf not specified, the first non-timestamp column will be taken.\n",
    "type": "string",
    "example": "y"
  },
  "HolidayColumn": {
    "description": "Defines which column represents the holiday column, identified by name.\nIf not set, no column is defined as holiday column.\n",
    "type": "string",
    "example": "PH"
  },
  "PredictionFrom": {
    "example": {
      "base_unit": "sample",
      "value": 1
    },
    "default": {
      "base_unit": "sample",
      "value": 1
    },
    "description": "Defines the beginning of the forecasting horizon;\nall samples before of this forecasting horizon are skipped.\n",
    "allOf": [
      {
        "$ref": "#/definitions/ForecastingTimeUnit"
      }
    ]
  },
  "PredictionTo": {
    "example": {
      "base_unit": "sample",
      "value": 1
    },
    "default": {
      "base_unit": "sample",
      "value": 1
    },
    "description": "Defines the end of the forecasting horizon, specifying how far ahead TIM should forecast",
    "allOf": [
      {
        "$ref": "#/definitions/ForecastingTimeUnit"
      }
    ]
  },
  "TransformationsForecasting": {
    "description": "An enumeration of all transformation types TIM should use during feature engineering;\nif not provided, the TIM Engine will determine the optimal transformations automatically\n",
    "type": "array",
    "uniqueItems": true,
    "minItems": 1,
    "items": {
      "type": "string",
      "enum": [
        "exponential_moving_average",
        "rest_of_week",
        "periodic",
        "intercept",
        "piecewise_linear",
        "time_offsets",
        "polynomial",
        "identity",
        "simple_moving_average",
        "month",
        "trend",
        "day_of_week",
        "fourier",
        "public_holidays",
        "one_hot_encoding"
      ]
    },
    "example": [
      "exponential_moving_average",
      "rest_of_week",
      "periodic",
      "intercept",
      "piecewise_linear",
      "time_offsets",
      "polynomial",
      "identity",
      "public_holidays",
      "one_hot_encoding"
    ]
  },
  "DailyCycle": {
    "description": "Decides whether models should focus on respective times within the day (specific hours, quarter-hours, etc.); if not set, TIM will determine this property automatically using autocorrelation analysis\n",
    "type": "boolean",
    "example": false
  },
  "Normalization": {
    "description": "Determines whether predictors should be normalized (scaled by their mean and standard deviation); switching this setting off may improve the modeling of data with structural changes",
    "type": "boolean",
    "default": true
  },
  "TargetOffsets": {
    "description": "Specifies offsets of target used in the model building process. If it is set to *none*, no target offsets and features using target offset will be used in the model.\nIf it is set to *common* only common offsets of target for situations within one day will be used. *close* means, that for each situation the closest possible offsets of target will be used.\nIf it is set to *combined*, the *close* will be used for situation within the first two days and *common* will be used for further forecasting horizons. Generally, default value is *combined*,\nhowever if predictor_offsets are set to *close*, then target_offsets will be *close* as well or if allow_offsets is set to false, then *none* will be used.\n",
    "type": "string",
    "example": "combined",
    "enum": [
      "none",
      "common",
      "close",
      "combined"
    ]
  },
  "TargetOffsetsForNormalBehavior": {
    "description": "Specifies offsets of target used in the model building process. If it is set to *none*, no target offsets and features using target offset will be used in the model.\nIf it is set to *close* then closest possible offsets of target will be used.\n",
    "type": "string",
    "example": "common",
    "enum": [
      "none",
      "common"
    ]
  },
  "PredictorOffsets": {
    "description": "Specifies offsets of predictors used in the model building process. If it is not set or set to *common* only common offsets of predictors for situations within one day will be used.\n*close* means, that for each situation the closest possible offsets of predictors will be used. It is tradeoff between model complexity and training time.\n*common* is faster and usually sufficient in accuracy. If 'predictorOffesets' are set to *close*, then 'target_offsets' can be set to the *none* or *close*.\n",
    "type": "string",
    "default": "common",
    "example": "common",
    "enum": [
      "common",
      "close"
    ]
  },
  "MaxFeatureCount": {
    "description": "Determines the maximal possible number of terms/features in each model in the modelZoo; if not set, TIM will automatically calculate the complexity based on the sampling period of the dataset",
    "type": "integer",
    "format": "int32",
    "minimum": 1,
    "example": 20
  },
  "AllowOffsets": {
    "description": "Enables using offset transformations of predictors, for example useful for using information of influencers that are not available throughout the entire forecasting horizon",
    "type": "boolean",
    "default": true,
    "example": true
  },
  "ConfidenceLevel": {
    "description": "The configuration of confidence level for prediction intervals; a symmetric prediction interval with a specific confidence level given in percentage will be returned for all predictions",
    "type": "number",
    "format": "double",
    "minimum": 0,
    "maximum": 100,
    "default": 90,
    "example": 90
  },
  "Backtest": {
    "description": "Determines what types whether backtesting forecast should be returned or not. Production forecast is returned always.\n",
    "type": "boolean",
    "default": true
  },
  "PredictionBoundaries": {
    "type": "object",
    "description": "Allows setting an upper and lower boundary for predictions; if not provided, TIM will default to boundaries created based on the Inter-Quartile-Range of the target variable",
    "additionalProperties": false,
    "properties": {
      "type": {
        "type": "string",
        "enum": [
          "explicit",
          "none"
        ],
        "description": "Explicit boundaries for predictions"
      },
      "max_value": {
        "type": "number",
        "format": "double",
        "example": 100,
        "description": "The upper boundary (maximum value) for predictions"
      },
      "min_value": {
        "type": "number",
        "format": "double",
        "example": 0,
        "description": "The lower boundary (minimum value) for predictions"
      }
    }
  },
  "ImputeConfiguration": {
    "type": "object",
    "description": "Imputation configuration",
    "additionalProperties": false,
    "properties": {
      "common": {
        "$ref": "#/definitions/ImputationParameters"
      },
      "individual": {
        "type": "array",
        "uniqueItems": true,
        "minItems": 1,
        "items": {
          "type": "object",
          "additionalProperties": false,
          "properties": {
            "column_name": {
              "type": "string",
              "example": "Predictor"
            },
            "value": {
              "$ref": "#/definitions/ImputationParameters"
            }
          }
        }
      }
    }
  },
  "ImputationParameters": {
    "type": "object",
    "description": "Determines the imputation of missing data",
    "required": [
      "type",
      "max_gap_length"
    ],
    "additionalProperties": false,
    "properties": {
      "type": {
        "type": "string",
        "default": "linear",
        "enum": [
          "linear",
          "locf"
        ]
      },
      "max_gap_length": {
        "type": "integer",
        "minimum": 0,
        "default": 0,
        "description": "The maximum length of gaps (number of consecutive missing observations) in variables to impute"
      }
    }
  },
  "ForecastingTimeUnit": {
    "type": "object",
    "required": [
      "base_unit",
      "value"
    ],
    "additionalProperties": false,
    "properties": {
      "base_unit": {
        "type": "string",
        "description": "The base time unit",
        "enum": [
          "day",
          "hour",
          "minute",
          "second",
          "sample"
        ]
      },
      "value": {
        "type": "integer",
        "format": "int32",
        "example": 1,
        "minimum": 1,
        "description": "The number of base units"
      }
    }
  },
  "OffsetLimit": {
    "description": "The maximum limit for offsets, defines how far offsets are taken into account in the model building process; if not set TIM will determine this automatically",
    "type": "integer",
    "maximum": 0
  },
  "DataAlignment": {
    "description": "List of column names and timestamps of the last non-missing observation for given column.\nIf not provided, the last timestamp is taken from the dataset.\n",
    "type": "array",
    "items": {
      "type": "object",
      "required": [
        "column_name",
        "timestamp"
      ],
      "additionalProperties": false,
      "properties": {
        "column_name": {
          "type": "string",
          "example": "Predictor"
        },
        "timestamp": {
          "type": "string",
          "example": "2021-01-31 00:00:00Z"
        }
      },
      "minLength": 1
    }
  },
  "Range": {
    "type": "object",
    "required": [
      "from",
      "to"
    ],
    "properties": {
      "from": {
        "type": "string",
        "example": "2021-01-01 00:00:00Z",
        "description": "The lower limit (earliest timestamp) of the range"
      },
      "to": {
        "type": "string",
        "example": "2021-01-31 00:00:00Z",
        "description": "The upper limit (latest timestamp) of the range"
      }
    }
  },
  "TimeScaleConfiguration": {
    "description": "Defines the time scaling configuration.\n",
    "type": "object",
    "required": [
      "time_scale"
    ],
    "additionalProperties": false,
    "properties": {
      "time_scale": {
        "$ref": "#/definitions/TimeScaleTimeUnit"
      },
      "aggregations": {
        "$ref": "#/definitions/Aggregations"
      },
      "drop_empty_rows": {
        "type": "boolean",
        "default": true,
        "description": "If set to false, empty rows remain in the dataset."
      }
    }
  },
  "TimeScaleTimeUnit": {
    "description": "Defines the sampling period to which TIM should aggregate the dataset.\n",
    "type": "object",
    "required": [
      "base_unit",
      "value"
    ],
    "additionalProperties": false,
    "properties": {
      "base_unit": {
        "type": "string",
        "description": "The base time unit",
        "enum": [
          "month",
          "day",
          "hour",
          "minute",
          "second"
        ],
        "example": "hour"
      },
      "value": {
        "type": "integer",
        "format": "int32",
        "example": 1,
        "minimum": 1,
        "description": "The number of base units"
      }
    }
  },
  "ModelIndexes": {
    "description": "List of model indexes for which the RCA should be calculated.\n",
    "type": "array",
    "items": {
      "type": "integer",
      "minItems": 1,
      "uniqueItems": true,
      "minimum": 1,
      "example": [
        1
      ]
    }
  }
}
"""


def _load_schema():
    return json.loads(SCHEMAS_JSON)


def _add_defintions_to_schema(sub_schema):
    sub_schema["definitions"] = _schema.copy()


def _get_schema_for_endpoint(schema_name):
    sub_schema = _schema[schema_name].copy()
    _add_defintions_to_schema(sub_schema)
    return sub_schema


def validate_schema(instance, schema):
    try:
        validate(instance=instance, schema=schema)
    except ValidationError as err:
        raise TangentValidationError(err.message) from err


_schema = _load_schema()

imputation_schema = _get_schema_for_endpoint("ImputeConfiguration")
time_scale_schema = _get_schema_for_endpoint("TimeScaleConfiguration")
forecasting_build_model_schema = _get_schema_for_endpoint("BuildConfiguration")
forecasting_build_normal_behavior_model_schema = _get_schema_for_endpoint(
    "BuildNormalBehaviorConfiguration"
)
forecasting_predict_schema = _get_schema_for_endpoint("PredictConfiguration")
forecasting_rca_schema = _get_schema_for_endpoint("RCAConfiguration")
auto_forecasting_schema = _get_schema_for_endpoint("AutoForecastingConfiguration")
anomaly_detection_build_model_schema = _get_schema_for_endpoint(
    "BuildAnomalyDetectionConfiguration"
)

_schema.clear()
