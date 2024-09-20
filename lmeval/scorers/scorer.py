from pydantic import Field

from ..custom_model import CustomModel
from ..models import LMModel, LMAnswer
from ..question import Question

from ..enums import ScorerType, Modality


class Scorer(CustomModel):
    name: str = Field(default='')
    description: str = Field(default='')
    type: ScorerType   # the enum type of the scorer used for serialization
    modality: Modality # what type of answer this scorer is for e.g text or multimodal

    # optional fields used only by specific scorers
    regex: str = Field(default='')
    model: LMModel | None = Field(default=None)


    def score(self, model_answer: LMAnswer, question: Question, task) -> float:
        raise NotImplementedError

    def _cleanup(self, txt: str) -> str:
        "Clean up text for comparison"
        txt = txt.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
        txt = ' '.join(txt.split()).strip()  # remove multiple spaces
        return txt

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return str(self)