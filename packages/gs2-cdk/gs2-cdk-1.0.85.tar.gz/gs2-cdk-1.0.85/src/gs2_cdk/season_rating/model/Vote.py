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
from .WrittenBallot import WrittenBallot
from .options.VoteOptions import VoteOptions


class Vote:
    season_name: str
    session_name: str
    written_ballots: Optional[List[WrittenBallot]] = None
    revision: Optional[int] = None

    def __init__(
        self,
        season_name: str,
        session_name: str,
        options: Optional[VoteOptions] = VoteOptions(),
    ):
        self.season_name = season_name
        self.session_name = session_name
        self.written_ballots = options.written_ballots if options.written_ballots else None
        self.revision = options.revision if options.revision else None

    def properties(
        self,
    ) -> Dict[str, Any]:
        properties: Dict[str, Any] = {}

        if self.season_name is not None:
            properties["seasonName"] = self.season_name
        if self.session_name is not None:
            properties["sessionName"] = self.session_name
        if self.written_ballots is not None:
            properties["writtenBallots"] = [
                v.properties(
                )
                for v in self.written_ballots
            ]

        return properties
