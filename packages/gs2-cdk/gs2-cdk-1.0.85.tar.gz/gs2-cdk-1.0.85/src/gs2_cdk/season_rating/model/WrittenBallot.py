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
from .Ballot import Ballot
from .GameResult import GameResult
from .options.WrittenBallotOptions import WrittenBallotOptions


class WrittenBallot:
    ballot: Ballot
    game_results: Optional[List[GameResult]] = None

    def __init__(
        self,
        ballot: Ballot,
        options: Optional[WrittenBallotOptions] = WrittenBallotOptions(),
    ):
        self.ballot = ballot
        self.game_results = options.game_results if options.game_results else None

    def properties(
        self,
    ) -> Dict[str, Any]:
        properties: Dict[str, Any] = {}

        if self.ballot is not None:
            properties["ballot"] = self.ballot.properties(
            )
        if self.game_results is not None:
            properties["gameResults"] = [
                v.properties(
                )
                for v in self.game_results
            ]

        return properties
