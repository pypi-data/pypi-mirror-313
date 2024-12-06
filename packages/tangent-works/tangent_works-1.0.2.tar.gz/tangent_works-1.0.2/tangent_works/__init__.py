"""
Tangent is the Predictive AI for your daily predictions - delivering instant insights at scale at a fraction of the cost.

Classes
----------
TimeSeries
    A class used to represent a time series dataset.
Forecasting
    A class used to build forecasting models and make forecasts.
AutoForecasting
    A class used to to perform auto forecasting.
AnomalyDetection
    A class used to build anomaly detection models and detect anomalies.
PostProcessing
    A class used to do post-processing models and forecasting results.
"""

from .__version__ import (
    __title__,
    __description__,
    __url__,
    __version__,
)

from tangent_works.business_data.time_series import TimeSeries
from tangent_works.api.forecasting import ForecastingApi as Forecasting
from tangent_works.api.auto_forecasting import AutoForecastingApi as AutoForecasting
from tangent_works.api.anomaly_detection import AnomalyDetectionApi as AnomalyDetection
from tangent_works.api.post_processing import PostProcessingApi as PostProcessing
