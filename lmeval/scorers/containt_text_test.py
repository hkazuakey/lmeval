from lmeval.scorers import get_scorer
from lmeval import ScorerType

from .utils import eval_question_answer

def test_contains_sensitive():
    # !you need to test symetrically to test both sides (model answer and true answer) are properly processed

    scorer = get_scorer(ScorerType.contain_text_sensitive)

    # expected good
    GOOD_ANSWERS_PAIRS = [['no', 'no'], ['no', ' no '], ['no', '=-no=-']]
    for pair in GOOD_ANSWERS_PAIRS:
        real_answer, model_answer = pair
        assert eval_question_answer(real_answer, model_answer, scorer) == 1.0

    # bad answers
    BAD_ANSWERS_PAIRS = [['no', 'yes'], ['no', 'No'], ['No', 'no'],  ['no', 'N o']]
    for pair in BAD_ANSWERS_PAIRS:
        real_answer, model_answer = pair
        assert eval_question_answer(real_answer, model_answer, scorer) == 0.0


def test_exact_insensitive():
    # !you need to test symetrically to test both sides (model answer and true answer) are properly processed

    scorer = get_scorer(ScorerType.contain_text_insensitive)

    # expected good
    GOOD_ANSWERS_PAIRS = [['no', 'no'], ['no', ' No '], ['no', '=-nO=-']]
    for pair in GOOD_ANSWERS_PAIRS:
        real_answer, model_answer = pair
        assert eval_question_answer(real_answer, model_answer, scorer) == 1.0

    # bad answers
    BAD_ANSWERS_PAIRS = [['no', 'yes'], ['no', 'N o']]
    for pair in BAD_ANSWERS_PAIRS:
        real_answer, model_answer = pair
        assert eval_question_answer(real_answer, model_answer, scorer) == 0.0