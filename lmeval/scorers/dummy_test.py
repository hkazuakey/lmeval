from lmeval.scorers import get_scorer
from lmeval import ScorerType

from .utils import eval_question_answer

def test_always_1():
    scorer = get_scorer(ScorerType.always_1)

    # correct
    real_answer = 'no'
    model_answer = 'no'
    assert eval_question_answer(real_answer, model_answer, scorer)== 1.0

    # incorrect
    BAD_ANSWERS_PAIRS = [['no', 'yes'], ['No', 'no']]
    for pair in BAD_ANSWERS_PAIRS:
        real_answer, model_answer = pair
        assert eval_question_answer(real_answer, model_answer, scorer) == 1.0

def test_always_0():
    scorer = get_scorer(ScorerType.always_0)

    # correct
    real_answer = 'no'
    model_answer = 'no'
    assert eval_question_answer(real_answer, model_answer, scorer)== 0.0

    # incorrect
    BAD_ANSWERS_PAIRS = [['no', 'yes'], ['No', 'no']]
    for pair in BAD_ANSWERS_PAIRS:
        real_answer, model_answer = pair
        assert eval_question_answer(real_answer, model_answer, scorer) == 0.0