from .scorer import Scorer
from ..question import Question
from ..models import LMAnswer

from ..enums import ScorerType, Modality


class TextExactSensitive(Scorer):
    name: str = ScorerType.text_exact_sensitive.name
    description: str  = "Returns 1.0 if the case-sensitive real answer and the model answer are exactly the same case sensitive"
    type: ScorerType = ScorerType.text_exact_sensitive
    modality: Modality = Modality.text

    def score(self, model_answer: LMAnswer, question: Question, task, debug: bool = False) -> float:
        ma = self._cleanup(model_answer.answer)
        qa = self._cleanup(question.answer)

        if ma == qa:
            return 1.0
        else:
            return 0.0


class TextExactInsensitive(Scorer):
    name: str = ScorerType.text_exact_insensitive.name
    description: str  = "Returns 1.0 if the case-insensitive real answer and the model answer text are exactly the same"
    type: ScorerType = ScorerType.text_exact_insensitive
    modality: Modality = Modality.text

    def score(self, model_answer: LMAnswer, question: Question, task, debug: bool = False) -> float:
        ma = self._cleanup(model_answer.answer).lower()
        qa = self._cleanup(question.answer).lower()

        if ma == qa:
            return 1.0
        else:
            return 0.0
