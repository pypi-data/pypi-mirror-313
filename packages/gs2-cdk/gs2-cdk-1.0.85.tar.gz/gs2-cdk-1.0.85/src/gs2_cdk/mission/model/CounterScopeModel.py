# Copyright 2016- Game Server Services, Inc. or its affiliates. All Rights
# Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# or in the "license" file accompanying this file. This file is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.
from __future__ import annotations
from typing import *
from ...core.model import VerifyAction
from .options.CounterScopeModelOptions import CounterScopeModelOptions
from .options.CounterScopeModelScopeTypeIsResetTimingOptions import CounterScopeModelScopeTypeIsResetTimingOptions
from .options.CounterScopeModelScopeTypeIsVerifyActionOptions import CounterScopeModelScopeTypeIsVerifyActionOptions
from .options.CounterScopeModelResetTypeIsNotResetOptions import CounterScopeModelResetTypeIsNotResetOptions
from .options.CounterScopeModelResetTypeIsDailyOptions import CounterScopeModelResetTypeIsDailyOptions
from .options.CounterScopeModelResetTypeIsWeeklyOptions import CounterScopeModelResetTypeIsWeeklyOptions
from .options.CounterScopeModelResetTypeIsMonthlyOptions import CounterScopeModelResetTypeIsMonthlyOptions
from .enum.CounterScopeModelScopeType import CounterScopeModelScopeType
from .enum.CounterScopeModelResetType import CounterScopeModelResetType
from .enum.CounterScopeModelResetDayOfWeek import CounterScopeModelResetDayOfWeek


class CounterScopeModel:
    scope_type: CounterScopeModelScopeType
    reset_type: Optional[CounterScopeModelResetType] = None
    reset_day_of_month: Optional[int] = None
    reset_day_of_week: Optional[CounterScopeModelResetDayOfWeek] = None
    reset_hour: Optional[int] = None
    condition_name: Optional[str] = None
    condition: Optional[VerifyAction] = None

    def __init__(
        self,
        scope_type: CounterScopeModelScopeType,
        options: Optional[CounterScopeModelOptions] = CounterScopeModelOptions(),
    ):
        self.scope_type = scope_type
        self.reset_type = options.reset_type if options.reset_type else None
        self.reset_day_of_month = options.reset_day_of_month if options.reset_day_of_month else None
        self.reset_day_of_week = options.reset_day_of_week if options.reset_day_of_week else None
        self.reset_hour = options.reset_hour if options.reset_hour else None
        self.condition_name = options.condition_name if options.condition_name else None
        self.condition = options.condition if options.condition else None

    @staticmethod
    def scope_type_is_reset_timing(
        reset_type: CounterScopeModelResetType,
        options: Optional[CounterScopeModelScopeTypeIsResetTimingOptions] = CounterScopeModelScopeTypeIsResetTimingOptions(),
    ) -> CounterScopeModel:
        return CounterScopeModel(
            CounterScopeModelScopeType.RESET_TIMING,
            CounterScopeModelOptions(
                reset_type,
            ),
        )

    @staticmethod
    def scope_type_is_verify_action(
        condition_name: str,
        condition: VerifyAction,
        options: Optional[CounterScopeModelScopeTypeIsVerifyActionOptions] = CounterScopeModelScopeTypeIsVerifyActionOptions(),
    ) -> CounterScopeModel:
        return CounterScopeModel(
            CounterScopeModelScopeType.VERIFY_ACTION,
            CounterScopeModelOptions(
                condition_name,
                condition,
            ),
        )

    @staticmethod
    def reset_type_is_not_reset(
        scope_type: CounterScopeModelScopeType,
        options: Optional[CounterScopeModelResetTypeIsNotResetOptions] = CounterScopeModelResetTypeIsNotResetOptions(),
    ) -> CounterScopeModel:
        return CounterScopeModel(
            scope_type,
            CounterScopeModelOptions(
            ),
        )

    @staticmethod
    def reset_type_is_daily(
        scope_type: CounterScopeModelScopeType,
        reset_hour: int,
        options: Optional[CounterScopeModelResetTypeIsDailyOptions] = CounterScopeModelResetTypeIsDailyOptions(),
    ) -> CounterScopeModel:
        return CounterScopeModel(
            scope_type,
            CounterScopeModelOptions(
                reset_hour,
            ),
        )

    @staticmethod
    def reset_type_is_weekly(
        scope_type: CounterScopeModelScopeType,
        reset_day_of_week: CounterScopeModelResetDayOfWeek,
        reset_hour: int,
        options: Optional[CounterScopeModelResetTypeIsWeeklyOptions] = CounterScopeModelResetTypeIsWeeklyOptions(),
    ) -> CounterScopeModel:
        return CounterScopeModel(
            scope_type,
            CounterScopeModelOptions(
                reset_day_of_week,
                reset_hour,
            ),
        )

    @staticmethod
    def reset_type_is_monthly(
        scope_type: CounterScopeModelScopeType,
        reset_day_of_month: int,
        reset_hour: int,
        options: Optional[CounterScopeModelResetTypeIsMonthlyOptions] = CounterScopeModelResetTypeIsMonthlyOptions(),
    ) -> CounterScopeModel:
        return CounterScopeModel(
            scope_type,
            CounterScopeModelOptions(
                reset_day_of_month,
                reset_hour,
            ),
        )

    def properties(
        self,
    ) -> Dict[str, Any]:
        properties: Dict[str, Any] = {}

        if self.scope_type is not None:
            properties["scopeType"] = self.scope_type.value
        if self.reset_type is not None:
            properties["resetType"] = self.reset_type.value
        if self.reset_day_of_month is not None:
            properties["resetDayOfMonth"] = self.reset_day_of_month
        if self.reset_day_of_week is not None:
            properties["resetDayOfWeek"] = self.reset_day_of_week.value
        if self.reset_hour is not None:
            properties["resetHour"] = self.reset_hour
        if self.condition_name is not None:
            properties["conditionName"] = self.condition_name
        if self.condition is not None:
            properties["condition"] = self.condition.properties(
            )

        return properties
