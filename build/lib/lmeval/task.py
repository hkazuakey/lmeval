# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pydantic import Field
from typing import List

from lmeval.custom_model import CustomModel
from lmeval.question import Question
from lmeval.enums import TaskType, TaskLevel, MultiShotStrategy, Modality
from lmeval.scorers import Scorer


class Task(CustomModel):
    name: str
    description: str = Field(default='')

    # metadata
    type: TaskType
    modality: Modality = Field(default=Modality.text)
    level: TaskLevel = Field(default=TaskLevel.basic)

    # scorers
    num_shots: int = Field(default=1)  # how many answers
    multi_short_scoring_strategy: MultiShotStrategy = Field(default=MultiShotStrategy.single)
    scorer: Scorer
    additional_scorers: List[Scorer] = Field(default_factory=list)

    # questions
    # Potentially exclude if scalability and write custom code
    questions: List[Question] = Field(default_factory=list)


    def __eq__(self, other):
        if isinstance(other, Task):
            return self.name == other.name  # Assuming 'name' uniquely identifies a task
        return False

    def __hash__(self):
        return hash(self.name)  # Again, assuming 'name' uniquely identifies a task