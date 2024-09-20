import pytest
from lmeval.prompts import MultiChoicesPrompt
from lmeval import Question, Task, TaskType
from lmeval import get_scorer, ScorerType

def test_multi_choices():
    prompt = MultiChoicesPrompt()
    question_text = "What is the capital of France?"
    question = Question(id=1, question=question_text, answer="Paris",
                        choices=["London", "Berlin", "Madrid"])
    task = Task(name="City capital", type=TaskType.multiple_choices,
                scorer=get_scorer(ScorerType.contain_text_insensitive))
    rendered_prompt =  prompt.render(question, task)
    print(prompt.template)
    print(rendered_prompt)


    assert question_text in rendered_prompt
    for choice in question.choices:
        assert choice in rendered_prompt
    assert question.answer in rendered_prompt
    for c in  ['A', 'B', 'C', 'D']:
        assert f"\n{c}:" in rendered_prompt

    # check that the answer letter is tied to the correct answer
    assert f"{question.answer_letter}:{question.answer}" in rendered_prompt


def test_repeated_used_multi_choices():
    prompt = MultiChoicesPrompt()
    question_text = "What is the capital of France?"
    question = Question(id=1, question=question_text, answer="Paris",
                        choices=["London", "Berlin", "Madrid"])
    task = Task(name="City capital", type=TaskType.multiple_choices,
                scorer=get_scorer(ScorerType.contain_text_insensitive))

    initial_answer_letter = ""
    for _ in range(5):
        rendered_prompt = prompt.render(question, task)
        print(prompt.template)
        print(rendered_prompt)

        if not initial_answer_letter:
            initial_answer_letter = question.answer_letter

        # check the order doesn't change
        assert question.answer_letter == initial_answer_letter

        assert question_text in rendered_prompt
        for choice in question.choices:
            assert choice in rendered_prompt
        assert question.answer in rendered_prompt
        for c in  ['A', 'B', 'C', 'D']:
            assert f"\n{c}:" in rendered_prompt

        # check that the answer letter is tied to the correct answer
        assert f"{question.answer_letter}:{question.answer}" in rendered_prompt

def test_answer_in_choice_fail():
    "Ensure that the generation fail if the answers is in the list of other choices"
    prompt = MultiChoicesPrompt()
    question_text = "What is the capital of France?"
    question = Question(id=1, question=question_text, answer="Paris",
                        choices=["Paris", "Berlin", "Madrid"])
    task = Task(name="City capital", type=TaskType.multiple_choices,
                scorer=get_scorer(ScorerType.contain_text_insensitive))
    with pytest.raises(AssertionError):
        prompt.render(question, task)