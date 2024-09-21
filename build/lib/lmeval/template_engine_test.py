from lmeval.template_engine import TemplateEngine

class Question:
    def __init__(self, text):
        self.text = text

class Answer:
    def __init__(self, text):
        self.text = text

def test_template_engine():
    template_string = "{{ question.text }} {{ answer.text }}"

    q = "What is the capital of France?"
    a = "Paris"
    question = Question(q)
    answer = Answer(a)  # Create the Answer object with the answer text
    result = TemplateEngine(template_string).render(question=question, answer=answer)
    assert result == f"{q} {a}"