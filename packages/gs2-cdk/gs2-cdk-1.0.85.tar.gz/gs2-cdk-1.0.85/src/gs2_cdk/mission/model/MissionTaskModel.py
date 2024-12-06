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
from .TargetCounterModel import TargetCounterModel
from ...core.model import VerifyAction
from ...core.model import AcquireAction
from .options.MissionTaskModelOptions import MissionTaskModelOptions
from .options.MissionTaskModelVerifyCompleteTypeIsCounterOptions import MissionTaskModelVerifyCompleteTypeIsCounterOptions
from .options.MissionTaskModelVerifyCompleteTypeIsVerifyActionsOptions import MissionTaskModelVerifyCompleteTypeIsVerifyActionsOptions
from .enum.MissionTaskModelVerifyCompleteType import MissionTaskModelVerifyCompleteType
from .enum.MissionTaskModelTargetResetType import MissionTaskModelTargetResetType


class MissionTaskModel:
    name: str
    verify_complete_type: MissionTaskModelVerifyCompleteType
    counter_name: str
    target_value: int
    metadata: Optional[str] = None
    target_counter: Optional[TargetCounterModel] = None
    verify_complete_consume_actions: Optional[List[VerifyAction]] = None
    complete_acquire_actions: Optional[List[AcquireAction]] = None
    challenge_period_event_id: Optional[str] = None
    premise_mission_task_name: Optional[str] = None
    target_reset_type: Optional[MissionTaskModelTargetResetType] = None

    def __init__(
        self,
        name: str,
        verify_complete_type: MissionTaskModelVerifyCompleteType,
        counter_name: str,
        target_value: int,
        options: Optional[MissionTaskModelOptions] = MissionTaskModelOptions(),
    ):
        self.name = name
        self.verify_complete_type = verify_complete_type
        self.counter_name = counter_name
        self.target_value = target_value
        self.metadata = options.metadata if options.metadata else None
        self.target_counter = options.target_counter if options.target_counter else None
        self.verify_complete_consume_actions = options.verify_complete_consume_actions if options.verify_complete_consume_actions else None
        self.complete_acquire_actions = options.complete_acquire_actions if options.complete_acquire_actions else None
        self.challenge_period_event_id = options.challenge_period_event_id if options.challenge_period_event_id else None
        self.premise_mission_task_name = options.premise_mission_task_name if options.premise_mission_task_name else None
        self.target_reset_type = options.target_reset_type if options.target_reset_type else None

    @staticmethod
    def verify_complete_type_is_counter(
        name: str,
        counter_name: str,
        target_value: int,
        target_counter: TargetCounterModel,
        options: Optional[MissionTaskModelVerifyCompleteTypeIsCounterOptions] = MissionTaskModelVerifyCompleteTypeIsCounterOptions(),
    ) -> MissionTaskModel:
        return MissionTaskModel(
            name,
            MissionTaskModelVerifyCompleteType.COUNTER,
            counter_name,
            target_value,
            MissionTaskModelOptions(
                target_counter,
                options.metadata,
                options.verify_complete_consume_actions,
                options.complete_acquire_actions,
                options.challenge_period_event_id,
                options.premise_mission_task_name,
                options.target_reset_type,
            ),
        )

    @staticmethod
    def verify_complete_type_is_verify_actions(
        name: str,
        counter_name: str,
        target_value: int,
        options: Optional[MissionTaskModelVerifyCompleteTypeIsVerifyActionsOptions] = MissionTaskModelVerifyCompleteTypeIsVerifyActionsOptions(),
    ) -> MissionTaskModel:
        return MissionTaskModel(
            name,
            MissionTaskModelVerifyCompleteType.VERIFY_ACTIONS,
            counter_name,
            target_value,
            MissionTaskModelOptions(
                options.metadata,
                options.verify_complete_consume_actions,
                options.complete_acquire_actions,
                options.challenge_period_event_id,
                options.premise_mission_task_name,
                options.target_reset_type,
            ),
        )

    def properties(
        self,
    ) -> Dict[str, Any]:
        properties: Dict[str, Any] = {}

        if self.name is not None:
            properties["name"] = self.name
        if self.metadata is not None:
            properties["metadata"] = self.metadata
        if self.verify_complete_type is not None:
            properties["verifyCompleteType"] = self.verify_complete_type.value
        if self.target_counter is not None:
            properties["targetCounter"] = self.target_counter.properties(
            )
        if self.verify_complete_consume_actions is not None:
            properties["verifyCompleteConsumeActions"] = [
                v.properties(
                )
                for v in self.verify_complete_consume_actions
            ]
        if self.complete_acquire_actions is not None:
            properties["completeAcquireActions"] = [
                v.properties(
                )
                for v in self.complete_acquire_actions
            ]
        if self.challenge_period_event_id is not None:
            properties["challengePeriodEventId"] = self.challenge_period_event_id
        if self.premise_mission_task_name is not None:
            properties["premiseMissionTaskName"] = self.premise_mission_task_name
        if self.counter_name is not None:
            properties["counterName"] = self.counter_name
        if self.target_reset_type is not None:
            properties["targetResetType"] = self.target_reset_type.value
        if self.target_value is not None:
            properties["targetValue"] = self.target_value

        return properties
