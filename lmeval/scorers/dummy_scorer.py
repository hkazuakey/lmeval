from ..question import Question
from ..models import LMAnswer

from ..enums import ScorerType, Modality
from .scorer import Scorer

class Always0Scorer(Scorer):
    name: str = ScorerType.always_0.name
    description: str = "Always return 0.0 as score."
    type: ScorerType = ScorerType.always_0
    modality: Modality = Modality.multimodal

    def score(self, model_answer: LMAnswer, question: Question, task) -> float:
        return 0.0

class Always1Scorer(Scorer):
    name: str = ScorerType.always_1.name
    description: str = "Always return 1.0 as score."
    type: ScorerType = ScorerType.always_1
    modality: Modality = Modality.multimodal

    def score(self, model_answer: LMAnswer, question: Question, task) -> float:
        return 1.0
