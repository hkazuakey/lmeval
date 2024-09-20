from .prompt import Prompt
from .text_generation_prompts import QuestionOnlyPrompt, ChainOfThoughtsPrompt, SingleWordAnswerPrompt
from .adversarial_prompts import AdversarialChainOfThoughtsPrompt
from .boolean_prompts import TrueOrFalseAnswerPrompt
from .multi_choices_prompts import MultiChoicesPrompt
__all__ = [
            "Prompt",

            # boolean
            "TrueOrFalseAnswerPrompt",

            # multiple choices
            "MultiChoicesPrompt",

            # Text gen
            "QuestionOnlyPrompt",
            "ChainOfThoughtsPrompt",
            "SingleWordAnswerPrompt",

            # Adversarial
            "AdversarialChainOfThoughtsPrompt"

        ]
