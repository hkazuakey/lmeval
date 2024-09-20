from lmeval import list_scorers, get_scorer
from lmeval import ScorerType
from lmeval.scorers import Always0Scorer
def test_list_scorers():
    list_scorers()  # just making sure it doesn't crash as it is a display function


def test_get_scorer():
    c = get_scorer(ScorerType.always_0)
    assert isinstance(c, Always0Scorer)