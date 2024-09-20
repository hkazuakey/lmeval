from lmeval.prompts import Prompt, QuestionOnlyPrompt
from lmeval import Question, Task, TaskType
from lmeval import get_scorer, ScorerType


def test_prompt_render():

    question_text = "what is the capital of France?"
    task_name = "This is a test task."
    prompt_tpls = [
        ["This is a test prompt.", "This is a test prompt."],
        ["{{question.question}}", question_text],
        ["{{task.name}}", task_name],
    ]

    for prompt_tpl in prompt_tpls:
        prompt = Prompt(name="test", description='', version='1.0',
                        task_type=TaskType.text_generation,
                        url='', template=prompt_tpl[0])

        task = Task(name=task_name,
                    type=TaskType.text_generation,
                    scorer=get_scorer(ScorerType.always_1))
        question = Question(id=1, question=question_text, answer="Paris")
        assert prompt.render(question, task) == prompt_tpl[1]