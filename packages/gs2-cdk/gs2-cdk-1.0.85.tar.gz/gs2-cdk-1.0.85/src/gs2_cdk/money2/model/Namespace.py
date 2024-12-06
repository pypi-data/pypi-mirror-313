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

from ...core.model import CdkResource, Stack
from ...core.func import GetAttr
from .PlatformSetting import PlatformSetting
from ...core.model import ScriptSetting
from ...core.model import LogSetting

from ..ref.NamespaceRef import NamespaceRef
from .CurrentMasterData import CurrentMasterData
from .StoreContentModel import StoreContentModel
from .enum.NamespaceCurrencyUsagePriority import NamespaceCurrencyUsagePriority

from .options.NamespaceOptions import NamespaceOptions


class Namespace(CdkResource):
    stack: Stack
    name: str
    currency_usage_priority: NamespaceCurrencyUsagePriority
    shared_free_currency: bool
    platform_setting: PlatformSetting
    description: Optional[str] = None
    deposit_balance_script: Optional[ScriptSetting] = None
    withdraw_balance_script: Optional[ScriptSetting] = None
    log_setting: Optional[LogSetting] = None

    def __init__(
        self,
        stack: Stack,
        name: str,
        currency_usage_priority: NamespaceCurrencyUsagePriority,
        shared_free_currency: bool,
        platform_setting: PlatformSetting,
        options: Optional[NamespaceOptions] = NamespaceOptions(),
    ):
        super().__init__(
            "Money2_Namespace_" + name
        )

        self.stack = stack
        self.name = name
        self.currency_usage_priority = currency_usage_priority
        self.shared_free_currency = shared_free_currency
        self.platform_setting = platform_setting
        self.description = options.description if options.description else None
        self.deposit_balance_script = options.deposit_balance_script if options.deposit_balance_script else None
        self.withdraw_balance_script = options.withdraw_balance_script if options.withdraw_balance_script else None
        self.log_setting = options.log_setting if options.log_setting else None
        stack.add_resource(
            self,
        )


    def alternate_keys(
        self,
    ):
        return "name"

    def resource_type(
        self,
    ) -> str:
        return "GS2::Money2::Namespace"

    def properties(
        self,
    ) -> Dict[str, Any]:
        properties: Dict[str, Any] = {}

        if self.name is not None:
            properties["Name"] = self.name
        if self.currency_usage_priority is not None:
            properties["CurrencyUsagePriority"] = self.currency_usage_priority
        if self.description is not None:
            properties["Description"] = self.description
        if self.shared_free_currency is not None:
            properties["SharedFreeCurrency"] = self.shared_free_currency
        if self.platform_setting is not None:
            properties["PlatformSetting"] = self.platform_setting.properties(
            )
        if self.deposit_balance_script is not None:
            properties["DepositBalanceScript"] = self.deposit_balance_script.properties(
            )
        if self.withdraw_balance_script is not None:
            properties["WithdrawBalanceScript"] = self.withdraw_balance_script.properties(
            )
        if self.log_setting is not None:
            properties["LogSetting"] = self.log_setting.properties(
            )

        return properties

    def ref(
        self,
    ) -> NamespaceRef:
        return NamespaceRef(
            self.name,
        )

    def get_attr_namespace_id(
        self,
    ) -> GetAttr:
        return GetAttr(
            self,
            "Item.NamespaceId",
            None,
        )

    def master_data(
        self,
        store_content_models: List[StoreContentModel],
    ) -> Namespace:
        CurrentMasterData(
            self.stack,
            self.name,
            store_content_models,
        ).add_depends_on(
            self,
        )
        return self
