from lmeval.prompts import TrueOrFalseAnswerPrompt
from lmeval import Question, Task, TaskType
from lmeval import get_scorer, ScorerType

def test_true_false():
    prompt = TrueOrFalseAnswerPrompt()
    question_text = "France is the capital of France?"
    question = Question(id=1, question=question_text, answer="True")
    task = Task(name="City capital", type=TaskType.boolean,
                scorer=get_scorer(ScorerType.contain_text_insensitive))
    rendered_prompt =  prompt.render(question, task)
    assert question_text in rendered_prompt
    assert 'false' in rendered_prompt.lower()

