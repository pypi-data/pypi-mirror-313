#
# Copyright 2021-2022 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from typing import Optional

from datarobot import errors
from datarobot._experimental.models.incremental_learning import IncrementalLearningMetadata
from datarobot.models import DatetimeModel as datarobot_datetime_model
from datarobot.models import FeatureEffects
from datarobot.models import Model as datarobot_model
from datarobot.utils import get_id_from_response


class Model(datarobot_model):  # pylint: disable=missing-class-docstring
    # pylint: disable=arguments-differ
    def get_feature_effect(self, source):
        """
        Retrieve Feature Effects for the model.

        Feature Effects provides partial dependence and predicted vs actual values for top-500
        features ordered by feature impact score.

        The partial dependence shows marginal effect of a feature on the target variable after
        accounting for the average effects of all other predictive features. It indicates how,
        holding all other variables except the feature of interest as they were,
        the value of this feature affects your prediction.

        Requires that Feature Effects has already been computed with
        :meth:`request_feature_effect <datarobot.models.Model.request_feature_effect>`.

        See :meth:`get_feature_effect_metadata <datarobot.models.Model.get_feature_effect_metadata>`
        for retrieving information the available sources.

        Parameters
        ----------
        source : string
            The source Feature Effects are retrieved for.


        Returns
        -------
        feature_effects : FeatureEffects
           The feature effects data.

        Raises
        ------
        ClientError (404)
            If the feature effects have not been computed or source is not valid value.
        """
        params = {"source": source}
        fe_url = self._get_feature_effect_url()
        server_data = self._client.get(fe_url, params=params).json()
        return FeatureEffects.from_server_data(server_data)

    def get_incremental_learning_metadata(self):
        """
        Retrieve incremental learning metadata for this model.

        .. versionadded:: v3.4.0

        This functionality requires the INCREMENTAL_LEARNING feature flag to be enabled.

        Returns
        -------
        metadata : IncrementalLearningMetadata
            a :py:class:`IncrementalLearningMetadata
            <datarobot._experimental.models.incremental_learning.IncrementalLearningMetadata>`
            representing incremental learning metadata
        """
        url = "projects/{}/models/{}/incrementalLearningMetadata/".format(self.project_id, self.id)
        server_data = self._client.get(url).json()
        server_data["projectId"] = self.project_id
        server_data["modelId"] = self.id
        return IncrementalLearningMetadata.from_server_data(server_data)

    def start_incremental_learning(self, early_stopping_rounds: Optional[int] = None) -> None:
        """
        Start incremental learning for this model.

        .. versionadded:: v3.4.0

        This functionality requires the INCREMENTAL_LEARNING feature flag to be enabled.

        Parameters
        ----------
        early_stopping_rounds: Optional[int]
            The number of chunks in which no improvement is observed that triggers the early stopping mechanism.

        Returns
        -------
        None

        Raises
        ------
        ClientError
            if the server responded with 4xx status

        """
        url = "projects/{}/incrementalLearningModels/incrementalTrain/".format(self.project_id)

        payload = {
            "modelId": self.id,
        }

        if early_stopping_rounds:
            payload["earlyStoppingRounds"] = early_stopping_rounds
        response = self._client.post(url, data=payload)

        error_msg = response.json().get(
            "message", "Incremental learning failed to start due to an error."
        )

        if response.status_code == 200:
            return
        else:
            raise errors.ClientError(
                error_msg + f" Server returned status {response.status_code}",
                response.status_code,
            )

    def train_first_incremental_from_sample(
        self,
    ):
        """Submit a job to the queue to perform the first incremental learning iteration training on an existing
        sample model. This functionality requires the SAMPLE_DATA_TO_START_PROJECT feature flag to be enabled.

        Returns
        -------
        job : ModelJob
            The created job that is retraining the model
        """
        from ...models.modeljob import (  # pylint: disable=import-outside-toplevel,cyclic-import
            ModelJob,
        )

        url = f"projects/{self.project_id}/incrementalLearningModels/fromSampleModel/"
        payload = {
            "modelId": self.id,
        }
        response = self._client.post(url, data=payload)
        return ModelJob.from_id(self.project_id, get_id_from_response(response))


class DatetimeModel(datarobot_datetime_model):  # pylint: disable=missing-class-docstring
    # pylint: disable-next=arguments-differ
    def get_feature_effect(self, source, backtest_index):
        """
        Retrieve Feature Effects for the model.

        Feature Effects provides partial dependence and predicted vs actual values for top-500
        features ordered by feature impact score.

        The partial dependence shows marginal effect of a feature on the target variable after
        accounting for the average effects of all other predictive features. It indicates how,
        holding all other variables except the feature of interest as they were,
        the value of this feature affects your prediction.

        Requires that Feature Effects has already been computed with
        :meth:`request_feature_effect <datarobot.models.Model.request_feature_effect>`.

        See :meth:`get_feature_effect_metadata \
        <datarobot.models.DatetimeModel.get_feature_effect_metadata>`
        for retrieving information of source, backtest_index.

        Parameters
        ----------
        source: string
            The source Feature Effects are retrieved for.
            One value of [FeatureEffectMetadataDatetime.sources]. To retrieve the available
            sources for feature effect.

        backtest_index: string, FeatureEffectMetadataDatetime.backtest_index.
            The backtest index to retrieve Feature Effects for.

        Returns
        -------
        feature_effects: FeatureEffects
           The feature effects data.

        Raises
        ------
        ClientError (404)
            If the feature effects have not been computed or source is not valid value.
        """
        params = {
            "source": source,
            "backtestIndex": backtest_index,
        }
        fe_url = self._get_feature_effect_url()
        server_data = self._client.get(fe_url, params=params).json()
        return FeatureEffects.from_server_data(server_data)
