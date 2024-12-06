#
# Copyright 2021 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from __future__ import annotations

from typing import List

from strenum import StrEnum

# pylint: disable=unused-import
from datarobot.enums import (  # noqa: F401
    ListChatsSortQueryParams,
    ListComparisonChatsSortQueryParams,
    ListCustomModelValidationsSortQueryParams,
    ListLLMBlueprintsSortQueryParams,
    ListPlaygroundsSortQueryParams,
    ListVectorDatabasesSortQueryParams,
    ModerationGuardAction,
    ModerationGuardConditionOperator,
    NemoLLMType,
    PromptType,
    VectorDatabaseChunkingParameterType,
    VectorDatabaseDatasetLanguages,
    VectorDatabaseEmbeddingModel,
    VectorDatabaseExecutionStatus,
    VectorDatabaseSource,
)

# pylint: enable=unused-import


class VectorDatabaseChunkingMethod(StrEnum):
    """Text chunking method names for VectorDatabases."""

    RECURSIVE = "recursive"
    SEMANTIC = "semantic"


class AllEnumMixin:
    @classmethod
    def all(cls) -> List[str]:
        return [member.value for _, member in cls.__members__.items()]


class NotebookType(AllEnumMixin, StrEnum):
    STANDALONE = "plain"
    CODESPACE = "codespace"


class RunType(StrEnum):
    SCHEDULED = "scheduled"
    MANUAL = "manual"


class ScheduledRunStatus(StrEnum):
    """Possible statuses for scheduled notebook runs."""

    BLOCKED = "BLOCKED"
    CREATED = "CREATED"
    STARTED = "STARTED"
    EXPIRED = "EXPIRED"
    ABORTED = "ABORTED"
    INCOMPLETE = "INCOMPLETE"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    INITIALIZED = "INITIALIZED"
    COMPLETED = "COMPLETED"
    ERROR = "ERROR"
    COMPLETED_WITH_ERRORS = "COMPLETED_WITH_ERRORS"

    @classmethod
    def terminal_statuses(cls) -> List[str]:
        return [
            cls.ABORTED,
            cls.COMPLETED,
            cls.ERROR,
            cls.COMPLETED_WITH_ERRORS,
        ]


class NotebookPermissions(StrEnum):
    CAN_READ = "CAN_READ"
    CAN_UPDATE = "CAN_UPDATE"
    CAN_DELETE = "CAN_DELETE"
    CAN_SHARE = "CAN_SHARE"
    CAN_COPY = "CAN_COPY"
    CAN_EXECUTE = "CAN_EXECUTE"


class NotebookStatus(StrEnum):
    STOPPING = "stopping"
    STOPPED = "stopped"
    STARTING = "starting"
    RUNNING = "running"
    RESTARTING = "restarting"
    DEAD = "dead"
    DELETED = "deleted"


class IncrementalLearningStatus(object):
    STARTED = "started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    STOPPED = "stopped"
    ERROR = "error"

    ALL = [STARTED, IN_PROGRESS, COMPLETED, STOPPED, ERROR]


class IncrementalLearningItemStatus(object):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ERROR = "error"

    ALL = [IN_PROGRESS, COMPLETED, ERROR]


class StorageType(StrEnum):
    """Supported data storages."""

    SNOWFLAKE = "snowflake"
    BIGQUERY = "bigquery"
    DATABRICKS = "databricks"
    AI_CATALOG = "aicatalog"
    DATASTAGE = "datastage"


class OriginStorageType(StrEnum):
    """Supported data sources."""

    SNOWFLAKE = StorageType.SNOWFLAKE
    BIGQUERY = StorageType.BIGQUERY
    DATABRICKS = StorageType.DATABRICKS
    AI_CATALOG = StorageType.AI_CATALOG


class ChunkingType(StrEnum):
    """Supported chunking types."""

    INCREMENTAL_LEARNING = "incrementalLearning"
    INCREMENTAL_LEARNING_OTV = "incrementalLearningOtv"
    SLICED_OFFSET_LIMIT = "slicedOffsetLimit"


class ChunkStorageType(StrEnum):
    """Supported chunk storage."""

    DATASTAGE = StorageType.DATASTAGE
    AI_CATALOG = StorageType.AI_CATALOG


class ChunkServiceDialect(StrEnum):
    SNOWFLAKE = "snowflake"
    BIGQUERY = "bigquery"
    DATABRICKS = "databricks"
    SPARK = "spark"
    POSTGRES = "postgres"


class ChunkingStrategy(StrEnum):
    FEATURES = "features"
    ROWS = "rows"


class ChunkingPartitionMethod(StrEnum):
    RANDOM = "random"
    STRATIFIED = "stratified"
    DATE = "date"


class FeedbackSentiment(StrEnum):
    POSITIVE = "1"
    NEGATIVE = "0"


class GuardConditionComparator(StrEnum):
    """The comparator used in a guard condition."""

    GREATER_THAN = "greaterThan"
    LESS_THAN = "lessThan"
    EQUALS = "equals"
    NOT_EQUALS = "notEquals"
    IS = "is"
    IS_NOT = "isNot"
    MATCHES = "matches"
    DOES_NOT_MATCH = "doesNotMatch"
    CONTAINS = "contains"
    DOES_NOT_CONTAIN = "doesNotContain"


class AggregationType(StrEnum):
    """The type of the metric aggregation."""

    AVERAGE = "average"
    BINARY_PERCENTAGE = "percentYes"
    MULTICLASS_PERCENTAGE = "classPercentCoverage"
    NGRAM_IMPORTANCE = "ngramImportance"
    GUARD_CONDITION_PERCENTAGE = "guardConditionPercentYes"


class GuardType(StrEnum):
    """The type of the guard configuration used for moderation in production."""

    MODEL = "guardModel"
    NEMO = "nemo"  # NVidia NeMo
    OOTB = "ootb"  # 'Out of the box' metric, little or no configuration
    PII = "pii"
    USER_MODEL = "userModel"  # user-defined columns and target type


class VectorDatabaseRetrievers(StrEnum):
    """Vector database retriever names."""

    SINGLE_LOOKUP_RETRIEVER = "SINGLE_LOOKUP_RETRIEVER"
    CONVERSATIONAL_RETRIEVER = "CONVERSATIONAL_RETRIEVER"
    MULTI_STEP_RETRIEVER = "MULTI_STEP_RETRIEVER"


class LLMTestConfigurationType(StrEnum):
    """Supported LLM test configuration types."""

    CUSTOM = "custom"
    OOTB = "ootb"


class GradingResult(StrEnum):
    """Supported LLM test grading results."""

    PASS = "PASS"
    FAIL = "FAIL"


class PromptSamplingStrategy(StrEnum):
    """The prompt sampling strategy for the evaluation dataset configuration."""

    RANDOM_WITHOUT_REPLACEMENT = "random_without_replacement"
    FIRST_N_ROWS = "first_n_rows"


class ModerationGuardType(StrEnum):
    """guard type"""

    MODEL = "guardModel"
    NEMO = "nemo"  # NVidia NeMo
    OOTB = "ootb"  # 'Out of the box' metric, little or no configuration
    PII = "pii"
    USER_MODEL = "userModel"  # user-defined columns and target type


class ModerationGuardConditionLogic(StrEnum):
    """condition logic"""

    ANY = "any"


class ModerationGuardStage(StrEnum):
    """guard stage"""

    PROMPT = "prompt"
    RESPONSE = "response"


class ModerationGuardModelTargetType(StrEnum):
    BINARY = "Binary"
    REGRESSION = "Regression"
    MULTICLASS = "Multiclass"
    TEXT_GENERATION = "TextGeneration"


class ModerationGuardOotbType(StrEnum):
    TOKEN_COUNT = "token_count"
    FAITHFULNESS = "faithfulness"
    ROUGE_1 = "rouge_1"


class ModerationGuardLlmType(StrEnum):
    OPEN_AI = "openAi"
    AZURE_OPEN_AI = "azureOpenAi"


class ModerationTimeoutActionType(StrEnum):
    BLOCK = "block"
    SCORE = "score"


class ModerationGuardEntityType(StrEnum):
    """Defines entity types the guards are associated with"""

    CUSTOM_MODEL = "customModel"
    CUSTOM_MODEL_VERSION = "customModelVersion"
    PLAYGROUND = "playground"
