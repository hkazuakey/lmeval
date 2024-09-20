from .scorer import Scorer
from ..question import Question
from ..models import LMAnswer

from ..enums import ScorerType, Modality


class ContainTextSensitive(Scorer):
    name: str = ScorerType.contain_text_sensitive.name
    description: str  = "Returns 1.0 if the case-sensitive model answer text is present in the real answer"
    type: ScorerType = ScorerType.contain_text_sensitive
    modality: Modality = Modality.text

    def score(self, model_answer: LMAnswer, question: Question, task, debug: bool = False) -> float:
        ma = self._cleanup(model_answer.answer)
        qa = self._cleanup(question.answer)

        if qa in ma:
            return 1.0
        else:
            return 0.0


class ContainTextInsensitive(Scorer):
    name: str = ScorerType.contain_text_insensitive.name
    description: str  = "Returns 1.0 if the case-insensitive model answer text is present in the real answer"
    type: ScorerType = ScorerType.contain_text_insensitive
    modality: Modality = Modality.text

    def score(self, model_answer: LMAnswer, question: Question, task, debug: bool = False) -> float:
        ma = self._cleanup(model_answer.answer).lower()
        qa = self._cleanup(question.answer).lower()
        if qa in ma:
            return 1.0
        else:
            return 0.0


