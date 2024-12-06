#
# Copyright 2023 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from typing import List, Optional

import trafaret as t
from typing_extensions import TypedDict

from datarobot._compat import String
from datarobot._experimental.models.enums import (
    IncrementalLearningItemStatus,
    IncrementalLearningStatus,
)
from datarobot.models.api_object import APIObject

IncrementalLearningItemDoc = t.Dict(
    {
        t.Key("chunk_index"): t.Int,
        t.Key("data_stage_id"): t.String,
        t.Key("status"): t.Enum(*IncrementalLearningItemStatus.ALL),
        t.Key("model_id"): t.String,
        t.Key("parent_model_id"): t.String,
        t.Key("sample_pct", optional=True): t.Float,
        t.Key("training_row_count", optional=True): t.Int,
        t.Key("score", optional=True): t.Float,
    }
).ignore_extra("*")


class IncrementalLearningItem(TypedDict):
    chunk_index: int
    data_stage_id: str
    status: str
    model_id: str
    parent_model_id: str
    sample_pct: Optional[float]
    training_row_count: Optional[int]
    score: Optional[float]


class IncrementalLearningMetadata(APIObject):
    """
    Incremental learning metadata for an incremental model.

    .. versionadded:: v3.4.0

    Attributes
    ----------
    project_id: string
        The project ID.
    model_id: string
        The model ID.
    user_id: string
        The ID of the user who started incremental learning.
    featurelist_id: string
        The ID of the featurelist the model is using.
    status: string
        The status of incremental training. One of ``datarobot._experimental.models.enums.IncrementalLearningStatus``.
    items: List[IncrementalLearningItemDoc]
        An array of incremental learning items associated with the sequential order of chunks.
        See incremental item info in `Notes` for more details.
    sample_pct: float
        The sample size in percents (1 to 100) to use in training.
    training_row_count: int
        The number of rows used to train a model.
    score: float
        The validation score of the model.
    metric: str
        The name of the scoring metric.
    early_stopping_rounds: int
        The number of chunks in which no improvement is observed that triggers the early stopping mechanism.
    total_number_of_chunks: int
        The total number of chunks.
    model_number: int
        The number of the model in the project.

    Notes
    -----

    Incremental item is a dict containing the following:

    * chunk_index: int
        The incremental learning order in which chunks are trained.
    * status: str
        The status of training current chunk.
        One of ``datarobot._experimental.models.enums.IncrementalLearningItemStatus``
    * model_id: str
        The ID of the model associated with the current item (chunk).
    * parent_model_id: str
        The ID of the model based on which the current item (chunk) is trained.
    * data_stage_id: str
        The ID of the data stage.
    * sample_pct: float
        The cumulative percentage of the base dataset size used for training the model.
    * training_row_count: int
        The number of rows used to train a model.
    * score: float
        The validation score of the current model

    """

    _converter = t.Dict(
        {
            t.Key("project_id"): String,
            t.Key("model_id"): String,
            t.Key("user_id"): String,
            t.Key("featurelist_id"): String,
            t.Key("status"): t.Enum(*IncrementalLearningStatus.ALL),
            t.Key("items"): t.List(IncrementalLearningItemDoc),
            t.Key("early_stopping_rounds"): t.Int,
            t.Key("sample_pct", optional=True): t.Float,
            t.Key("training_row_count", optional=True): t.Int,
            t.Key("score", optional=True): t.Float,
            t.Key("metric", optional=True): t.String,
            t.Key("total_number_of_chunks", optional=True): t.Int,
            t.Key("model_number", optional=True): t.Int,
        }
    ).ignore_extra("*")

    def __init__(
        self,
        project_id: str,
        model_id: str,
        user_id: str,
        featurelist_id: str,
        status: str,
        items: List[IncrementalLearningItem],
        early_stopping_rounds: int,
        sample_pct: Optional[float] = None,
        training_row_count: Optional[int] = None,
        score: Optional[float] = None,
        metric: Optional[str] = None,
        total_number_of_chunks: Optional[int] = None,
        model_number: Optional[int] = None,
    ) -> None:
        self.project_id = project_id
        self.model_id = model_id
        self.user_id = user_id
        self.featurelist_id = featurelist_id
        self.status = status
        self.items = items
        self.sample_pct = sample_pct
        self.training_row_count = training_row_count
        self.score = score
        self.metric = metric
        self.early_stopping_rounds = early_stopping_rounds
        self.total_number_of_chunks = total_number_of_chunks
        self.model_number = model_number

    def __repr__(self) -> str:
        return "{}(project_id={}, model_id={})".format(
            self.__class__.__name__,
            self.project_id,
            self.model_id,
        )
