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