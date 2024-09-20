from .benchmark import Benchmark, Category, Task
from .question import Question
from .models import LMModel, LMAnswer
from .prompts import Prompt

class Callback():

    benchmark: Benchmark | None = None

    # called when the evaluation starts
    def on_evaluation_start(self, model: LMModel, prompt: Prompt) -> None:
        "Trigger when the evaluation starts"
        pass

    def on_evaluation_end(self, model: LMModel, prompt: Prompt) -> None:
        "Trigger when the evaluation ends"
        pass

    def on_category_start(self, category: Category) -> None:
        "Trigger when a category starts"
        pass

    def on_category_end(self, category: Category) -> None:
        "Trigger when a category ends"
        pass

    def on_task_start(self, task: Task) -> None:
        "Trigger when a task starts"
        pass

    def on_task_end(self, task: Task) -> None:
        "Trigger when a task ends"
        pass

    def on_question_start(self, question: Question, model: LMModel,
                          prompt: Prompt) -> None:
        "Trigger when a question starts"
        pass
    def on_question_end(self, question: Question, answer: LMAnswer,
                        model: LMModel, prompt: Prompt) -> None:
        "Trigger when a question ends"
        pass