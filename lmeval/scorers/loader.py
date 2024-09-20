from tabulate import tabulate
from .scorer import Scorer

from .dummy_scorer import Always1Scorer, Always0Scorer
from .boolean_answer import BooleanAnswerScorer
from .multiple_choices import ContainAnswerLetterInsensitive
from .exact_text import TextExactInsensitive, TextExactSensitive
from .regex import TextSensitiveRegex, TextInsensitiveRegex
from .contain_text import ContainTextSensitive, ContainTextInsensitive
from .punt_detector import PuntDetector
from ..enums import ScorerType


_SCORERS = {
    ScorerType.always_1: Always1Scorer,
    ScorerType.always_0: Always0Scorer,

    # boolean answer
    ScorerType.boolean_answer: BooleanAnswerScorer,

    # multiple choices
    ScorerType.contains_answer_letter_insensitive: ContainAnswerLetterInsensitive,

    # exact text
    ScorerType.text_exact_sensitive: TextExactSensitive,
    ScorerType.text_exact_insensitive: TextExactInsensitive,

    # contain text
    ScorerType.contain_text_sensitive: ContainTextSensitive,
    ScorerType.contain_text_insensitive: ContainTextInsensitive,

    # regex
    ScorerType.text_regex_sensitive: TextSensitiveRegex,
    ScorerType.text_regex_insensitive: TextInsensitiveRegex,

    # safety
    ScorerType.punt_detector: PuntDetector,
}

def get_scorer(scorer_type: ScorerType) -> Scorer:
    "get scorer object for a given scorer type"
    if scorer_type in _SCORERS:
        return _SCORERS[scorer_type]()
    else:
        raise ValueError(f"Unimplemented scorer {scorer_type}")

def list_scorers():
    "list all available scorers"
    rows = []
    for s in _SCORERS.values():
        si = s()
        rows.append([si.name, si.__class__.__name__ , si.modality.name, si.description])
    print(tabulate(rows, headers=["Name", "Class Name", "Modality", "Description"]))
