from io import StringIO
import json
from typing import Any, Callable, Dict, Optional
import pandas as pd
from tangent_works.business_data.anomaly_detection_configuration import (
    AnomalyDetectionBuildConfiguration,
)
from tangent_works.business_data.anomaly_detection_model import AnomalyDetectionModel
from tangent_works.business_data.time_series import TimeSeries
from tangent_works.utils.exceptions import TangentValidationError
from tangent_works.utils.python_client_utils import (
    send_rest_api_request,
    wait_for_job_to_finish,
)


class AnomalyDetectionApi:
    """
    A class used to build anomaly detection models and detect anomalies.

    Attributes
    ----------
    result_table : pd.DataFrame, optional
        Anomaly detection results table (is None when detect method was not called or new model was built).
    rca_table : pd.DataFrame, optional
        Root cause analysis table (is None when rca method was not called or new model was built).
    time_series : TimeSeries, optional
        Time series data used for building the model and detecting anomalies.
    configuration : AnomalyDetectionBuildConfiguration
        Configuration used for building the model.
    model : AnomalyDetectionModel, optional
        Anomaly detection model.

    Methods
    -------
    from_model(model):
        Creates AnomalyDetection object from existing model.
    build_model(inplace):
        Builds anomaly detection model.
    detect(time_series, inplace):
        Detects anomalies in the time series data.
    rca(configuration, time_series, inplace):
        Performs root cause analysis.
    """

    def __init__(
        self,
        time_series: Optional[TimeSeries] = None,
        configuration: Optional[Dict[str, Any]] = None,
    ):
        """
        Parameters
        ----------
        time_series : TimeSeries, optional
            Time series data used for building the model and detecting anomalies.
        configuration : Dict[str, Any], optional
            Configuration used for building the model.
        """

        if not isinstance(time_series, TimeSeries) and time_series is not None:
            raise TangentValidationError("Invalid time-series object type.")

        if not isinstance(configuration, Dict) and configuration is not None:
            raise TangentValidationError("Invalid configuration object type.")

        self._configuration_dict = configuration if configuration else {}
        self._configuration = self._create_build_configuration(self._configuration_dict)

        self._time_series = time_series
        self._model = None
        self._result_table = None
        self._rca_table = None

    def _create_build_configuration(
        self, configuration_input: Dict[str, Any]
    ) -> AnomalyDetectionBuildConfiguration:
        configuration = configuration_input.copy()
        if (
            "normal_behavior" in configuration
            and "max_offsets_depth" in configuration["normal_behavior"]
        ):
            configuration["normal_behavior"]["offset_limit"] = (
                -1 * configuration["normal_behavior"]["max_offsets_depth"]
            )
            configuration["normal_behavior"].pop("max_offsets_depth")

        return AnomalyDetectionBuildConfiguration.from_dict(configuration)

    @classmethod
    def from_model(
        cls, model: Dict[str, Any] | AnomalyDetectionModel
    ) -> "AnomalyDetectionApi":
        """
        Creates AnomalyDetection object from existing model.

        Parameters
        ----------
        model : Dict[str, Any] or AnomalyDetectionModel
            Anomaly detection model.

        Returns
        -------
        AnomalyDetectionApi
            New AnomalyDetection object.
        """

        obj = cls()
        if isinstance(model, AnomalyDetectionModel):
            obj._model = model
        elif isinstance(model, dict):
            obj._model = AnomalyDetectionModel.from_dict(model)
        else:
            raise TangentValidationError("Invalid model object type.")
        return obj

    @property
    def result_table(self) -> Optional[pd.DataFrame]:
        """
        Anomaly detection results table (is None when detect method was not called or new model was built).
        """

        return self._result_table

    @property
    def rca_table(self) -> Optional[pd.DataFrame]:
        """
        Root cause analysis table (is None when rca method was not called or new model was built).
        """

        return self._rca_table

    @property
    def time_series(self) -> Optional[TimeSeries]:
        """
        Time series data used for building the model and detecting anomalies.
        """

        return self._time_series

    @property
    def configuration(self) -> AnomalyDetectionBuildConfiguration:
        """
        Configuration used for building the model.
        """

        return self._configuration

    @property
    def model(self) -> Optional[AnomalyDetectionModel]:
        """
        Anomaly detection model.
        """

        return self._model

    def build_model(
        self,
        inplace: bool = True,
        status_poll: bool = True,
    ) -> None:
        """
        Builds anomaly detection model.

        Parameters
        ----------
        inplace : bool, optional
            If True, the method returns None. If False, the method returns the AnomalyDetection object reference.
        status_poll : bool, optional
            If True, the job status is periodically checked and printed to the console.

        Returns
        -------
        None or AnomalyDetection
            Returns None if inplace is True, otherwise returns the AnomalyDetection object reference.
        """

        self._result_table = None
        self._rca_table = None

        self._validate_build_model_call()

        dataset_csv = self._time_series.dataframe.to_csv(
            index=False, sep=",", decimal="."
        )

        metadata_dict = {
            "timestamp_column": self._time_series.timestamp,
            "group_key_columns": self._time_series.group_keys,
        }

        request_part = [
            ("dataset", ("dataset.csv", dataset_csv, "text/csv")),
            (
                "configuration",
                (
                    "configuration.json",
                    json.dumps(self._configuration_dict),
                    "application/json",
                ),
            ),
            (
                "metadata",
                (
                    "metadata.json",
                    json.dumps(metadata_dict),
                    "application/json",
                ),
            ),
        ]

        post_response = send_rest_api_request(
            "POST", "/anomaly-detection/build-model", request_part
        )
        job_id = post_response.json()["id"]
        wait_for_job_to_finish("anomaly-detection", job_id, status_poll=status_poll)

        model_response = send_rest_api_request(
            "GET", f"/anomaly-detection/{job_id}/model"
        )
        model_dict = model_response.json()
        self._model = AnomalyDetectionModel.from_dict(model_dict)

        if not inplace:
            return self

    def detect(
        self,
        time_series: Optional[TimeSeries] = None,
        inplace: bool = True,
        status_poll: bool = True,
    ) -> pd.DataFrame:
        """
        Detects anomalies in the time series data.

        Parameters
        ----------
        time_series : TimeSeries, optional
            Time series data used for detecting anomalies (if None, forecast is done on the same time series data as model building).
        inplace : bool, optional
            If True, the method returns pd.Dataframe containing anomaly detection results table. If False, the method returns the AnomalyDetection object reference.
        status_poll : bool, optional
            If True, the job status is periodically checked and printed to the console.

        Returns
        -------
        pd.DataFrame
            Anomaly detection results table.
        """

        self._result_table = None

        input_time_series = (
            time_series if time_series is not None else self._time_series
        )

        self._validate_detect_call(input_time_series)

        dataset_csv = input_time_series.dataframe.to_csv(
            index=False, sep=",", decimal="."
        )

        metadata_dict = {
            "timestamp_column": input_time_series.timestamp,
            "group_key_columns": input_time_series.group_keys,
        }

        request_part = [
            ("dataset", ("dataset.csv", dataset_csv, "text/csv")),
            (
                "model",
                (
                    "model.json",
                    json.dumps(self._model.to_dict()),
                    "application/json",
                ),
            ),
            (
                "metadata",
                (
                    "metadata.json",
                    json.dumps(metadata_dict),
                    "application/json",
                ),
            ),
        ]

        post_response = send_rest_api_request(
            "POST", "/anomaly-detection/detect", request_part
        )
        job_id = post_response.json()["id"]
        wait_for_job_to_finish("anomaly-detection", job_id, status_poll=status_poll)

        results_response = send_rest_api_request(
            "GET", f"/anomaly-detection/{job_id}/results"
        )
        self._result_table = pd.read_csv(
            StringIO(results_response.text), sep=None, engine="python"
        )

        if not inplace:
            return self
        return self._result_table

    def rca(
        self,
        configuration: Dict[str, Any] = None,
        time_series: Optional[TimeSeries] = None,
        inplace: bool = True,
        status_poll: bool = True,
    ) -> Dict[int, pd.DataFrame]:
        """
        Performs root cause analysis.

        Parameters
        ----------
        configuration : Dict[str, Any], optional
            RCA configuration (if None, RCA is done in fully automatic mode).
        time_series : TimeSeries, optional
            Time series data used for RCA (if None, RCA is done on the same time series data as model building).
        inplace : bool, optional
            If True, the method returns Dict[int, pd.DataFrame] containing RCA table. If False, the method returns the AnomalyDetection object reference.
        status_poll : bool, optional
            If True, the job status is periodically checked and printed to the console.

        Returns
        -------
        Dict[int, pd.DataFrame]
            RCA table.
        """

        self._rca_table = None

        input_time_series = (
            time_series if time_series is not None else self._time_series
        )
        config = configuration if configuration else {}

        self._validate_rca_call(config, input_time_series)

        dataset_csv = input_time_series.dataframe.to_csv(
            index=False, sep=",", decimal="."
        )

        metadata_dict = {
            "timestamp_column": input_time_series.timestamp,
            "group_key_columns": input_time_series.group_keys,
        }

        request_part = [
            ("dataset", ("dataset.csv", dataset_csv, "text/csv")),
            (
                "configuration",
                (
                    "configuration.json",
                    json.dumps(config),
                    "application/json",
                ),
            ),
            (
                "model",
                (
                    "model.json",
                    json.dumps(self._model.to_dict()),
                    "application/json",
                ),
            ),
            (
                "metadata",
                (
                    "metadata.json",
                    json.dumps(metadata_dict),
                    "application/json",
                ),
            ),
        ]

        post_response = send_rest_api_request(
            "POST", "/anomaly-detection/rca", request_part
        )
        job_id = post_response.json()["id"]
        wait_for_job_to_finish("anomaly-detection", job_id, status_poll=status_poll)

        rca_table_response = send_rest_api_request(
            "GET", f"/anomaly-detection/{job_id}/rca-table"
        )
        rca_table_dict = rca_table_response.json()
        rca_table = {}
        for key, value in rca_table_dict.items():
            rca_table[int(key)] = pd.read_csv(StringIO(value), sep=",", decimal=".")

        self._rca_table = rca_table
        if not inplace:
            return self
        return self._rca_table

    def _validate_build_model_call(self) -> None:
        if self.model is not None:
            raise TangentValidationError("The model has already been built.")

        if self.time_series is None or self.time_series.dataframe is None:
            raise TangentValidationError("The time-series object has not been set.")

    def _validate_detect_call(self, input_time_series: TimeSeries) -> None:
        if not isinstance(input_time_series, TimeSeries):
            raise TangentValidationError("Invalid time-series object type.")

        if input_time_series is None or input_time_series.dataframe is None:
            raise TangentValidationError("The time-series object has not been set.")

        if self.model is None:
            raise TangentValidationError(
                "The model has not been built. Please, first build the model."
            )

    def _validate_rca_call(
        self, configuration: Dict[str, Any], input_time_series: TimeSeries
    ) -> None:
        if not isinstance(configuration, Dict):
            raise TangentValidationError("Invalid configuration object type.")

        if not isinstance(input_time_series, TimeSeries):
            raise TangentValidationError("Invalid time-series object type.")

        if input_time_series is None or input_time_series.dataframe is None:
            raise TangentValidationError("The time-series object has not been set.")
