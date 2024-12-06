from typing import Any, Dict, Union
import pandas as pd
import numpy as np
from tangent_works.api.auto_forecasting import AutoForecastingApi
from tangent_works.api.forecasting import ForecastingApi


class PostProcessingApi:
    """
    A class used to do post-processing models and forecasting results.

    Methods
    -------
    result_table(forecasting):
        Extends the result table with additional information about training, testing, and production data.
    properties(response):
        Extracts variable properties from the model.
    features(response):
        Extracts features from the model-building response.
    """

    def result_table(
        self, forecasting: Union[ForecastingApi, AutoForecastingApi]
    ) -> pd.DataFrame:
        """
        Extends the result table with additional information about training, testing, and production data.

        Parameters
        ----------
        forecasting : Forecasting or AutoForecasting
            Forecasting object.

        Returns
        -------
        pd.DataFrame
            Post-processed results table.
        """

        configuration = forecasting.configuration
        df = forecasting.result_table.copy()
        df["timestamp"] = pd.to_datetime(df["timestamp"])

        target_name = forecasting.model.model_zoo.target_name
        timestamp_name = forecasting.time_series.timestamp
        dataframe = forecasting.time_series.dataframe
        last_target_timestamp = dataframe.iloc[dataframe[target_name].last_valid_index()][timestamp_name]

        production_ts = list(df[df['timestamp'] > last_target_timestamp]['timestamp'])
        timestamps = forecasting.time_series.timestamps

        try:
            if configuration.training_rows == None:
                training_ts = list(timestamps[timestamps <= last_target_timestamp])
            else:
                training_ts = self._get_timestamps(
                    rows=configuration.training_rows, series=timestamps
                )
        except:
            training_ts = list(timestamps[timestamps <= last_target_timestamp])

        testing_ts = list(
            df[
                ~(df["timestamp"].isin(training_ts))
                & ~(df["timestamp"].isin(production_ts))
            ]["timestamp"]
        )

        df["type"] = np.where(
            df["timestamp"].isin(production_ts),
            "production",
            np.where(
                df["timestamp"].isin(training_ts),
                "training",
                np.where(
                    df["timestamp"].isin(testing_ts), "testing", "undefined"
                ),
            ),
        )
        return df[
            ~((df["target"].isnull()) & (df["forecast"].isnull()))
        ]

    def properties(self, model: Dict[str, Any]) -> pd.DataFrame:
        """
        Extracts variable properties from the model-building response.

        Parameters
        ----------
        model : Dict[str, Any]
            A model-building response.

        Returns
        -------
        pd.DataFrame
            Variable properties.
        """

        try:
            properties = model["model_zoo"]["variable_properties"]
        except Exception:
            properties = model["normal_behavior_model"]["model_zoo"][
                "variable_properties"
            ]
        df = pd.DataFrame(properties).sort_values(by="importance", ascending=False)
        df["rel_importance"] = (
            df["importance"] / df.sum()["importance"]
        )  # pylint: disable=unsupported-assignment-operation, unsubscriptable-object
        return df

    def features(self, model: Dict[str, Any]) -> pd.DataFrame:
        """
        Extracts features from the model-building response.

        Parameters
        ----------
        model : Dict[str, Any]
            A model-building response.

        Returns
        -------
        pd.DataFrame
            Features.
        """

        try:
            models = model["model_zoo"]["models"]
        except Exception:
            models = model["normal_behavior_model"]["model_zoo"]["models"]
        features = []
        for m in models:
            terms = m["terms"]
            for count, term in enumerate(terms):
                feature, beta = self._find_feature(term["parts"])
                features.append([m["index"], count, feature, term["importance"], beta])
        return pd.DataFrame(
            features, columns=["model", "term", "feature", "importance", "beta"]
        )

    def _find_feature(self, sub_parts):
        dow_list = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]
        month_list = [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ]
        features_list = []
        beta = None
        for c, s in enumerate(sub_parts):
            if s["type"] == "β":
                sub_feature = ""
            elif s["type"] == "time_offsets":
                sub_feature = s["predictor"] + "(t" + str(s["offset"]) + ")"
            elif s["type"] == "rest_of_week":
                sub_feature = (
                    "DoW(t" + str(s["offset"]) + ") <= " + dow_list[s["day"] - 1]
                )
            elif s["type"] == "intercept":
                sub_feature = "Intercept(" + str(int(s["value"])) + ")"
            elif s["type"] == "cos":
                sub_feature = "Cos(" + str(int(s["period"])) + ";" + s["unit"] + ")"
            elif s["type"] == "sin":
                sub_feature = "Sin(" + str(int(s["period"])) + ";" + s["unit"] + ")"
            elif s["type"] == "exponential_moving_average":
                sub_feature = (
                    "EMA_"
                    + s["predictor"]
                    + "(t"
                    + str(int(s["offset"]))
                    + "; w="
                    + str(int(s["window"]))
                    + ")"
                )
            elif s["type"] == "identity":
                sub_feature = s["predictor"]
            elif s["type"] == "piecewise_linear":
                sub_feature = (
                    "Maximum(0;"
                    + str(s["subtype"])
                    + "*("
                    + str(round(s["knot"], 6))
                    + "-"
                    + s["predictor"]
                    + "(t"
                    + str(s["offset"])
                    + ")))"
                )
            elif s["type"] == "simple_moving_average":
                sub_feature = (
                    "SMA_"
                    + s["predictor"]
                    + "(t"
                    + str(int(s["offset"]))
                    + "; w="
                    + str(int(s["window"]))
                    + ")"
                )
            elif s["type"] == "fourier":
                sub_feature = "Fourier(" + str(s["period"]) + ")"
            elif s["type"] == "weekday":
                sub_feature = (
                    "DoW(t" + str(s["offset"]) + ") = " + dow_list[s["day"] - 1]
                )
            elif s["type"] == "month":
                sub_feature = "Month<=" + month_list[s["month"]]
            elif s["type"] == "public_holidays":
                sub_feature = s["predictor"]
            elif s["type"] == "trend":
                sub_feature = "Trend"
            else:
                sub_feature = "_test_"
            if s["type"] == "β":
                features_list.append(sub_feature)
                beta = s["value"]
            else:
                if c > 0:
                    features_list.append(" & " + sub_feature)
                else:
                    features_list.append(sub_feature)
        feature_output = "".join(str(e) for e in features_list)
        return feature_output, beta

    def _get_timestamps(self, rows, series):
        output = []
        for row in rows:
            output.append(list(series[(series >= min(row)) & (series <= max(row))]))
        return sorted(list(set(sum(output, []))))
