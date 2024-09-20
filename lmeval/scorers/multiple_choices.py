from .scorer import Scorer
from ..question import Question
from ..models import LMAnswer

from ..enums import ScorerType, Modality

class ContainAnswerLetterInsensitive(Scorer):
    name: str = ScorerType.contains_answer_letter_insensitive.name
    description: str  = "Returns 1.0 if the answer letter is present in the model answer"
    type: ScorerType = ScorerType.contains_answer_letter_insensitive
    modality: Modality = Modality.text

    def score(self, model_answer: LMAnswer, question: Question, task, debug: bool = False) -> float:
        assert question.answer_letter is not None, "Answer letter is not provided - this is scorer can only be used with Multiple Choice question Prompts."
        ma = self._cleanup(model_answer.answer).lower()
        qa = self._cleanup(question.answer_letter).lower()
        if qa in ma:
            return 1.0
        else:
            return 0.0


