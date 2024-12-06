#
# Copyright 2024 DataRobot, Inc. and its affiliates.
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

from typing import Any, Dict

import trafaret as t

from datarobot.enums import ModerationGuardConditionOperator
from datarobot.models.api_object import APIObject


class GuardInterventionCondition(APIObject):
    """Defines a condition for intervention."""

    _converter = t.Dict(
        {
            t.Key("comparator"): t.Enum(*[e.value for e in ModerationGuardConditionOperator]),
            t.Key("comparand"): t.Or(
                t.Float(),
                t.String(),
                t.Bool(),
                t.List(
                    t.String(),
                ),
            ),
        }
    ).ignore_extra("*")

    schema = _converter

    def __init__(self: GuardInterventionCondition, **kwargs: Any) -> None:
        self._set_values(**kwargs)

    def __repr__(self) -> str:
        return "{}(comparator={!r}, comparand={!r})".format(
            self.__class__.__name__,
            self.comparator,
            self.comparand,
        )

    def _set_values(
        self: GuardInterventionCondition,
        comparator: ModerationGuardConditionOperator,
        comparand: Any,
    ) -> None:
        self.comparator = ModerationGuardConditionOperator(comparator)
        self.comparand = comparand

    def to_dict(self) -> Dict[str, str]:
        return {
            "comparator": self.comparator.value,
            "comparand": self.comparand,
        }
