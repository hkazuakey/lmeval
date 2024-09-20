from lmeval import get_scorer, ScorerType, Question, Task, LMAnswer
from ..fixtures import gemini

def test_punt_detector(gemini):
    punt_detector = get_scorer(ScorerType.punt_detector)
    punt_detector.model = gemini

    question = Question(id=0, question='what is the capital of france?', answer='Paris')

    non_punt_answers = ['Paris', 'paris', 'paris?', 'Berlin',
                        "I am unsure", "I don't know"]
    gemini.set_default_response('answered')
    for answer in non_punt_answers:
        lmanswer = LMAnswer(answer=answer, raw_response=answer,
                            generation_time=0.0, model=gemini)
        print(answer)
        score = punt_detector.score(lmanswer, question, task=None)
        assert score == 0.0

    punt_answers = ["I can't answer", "I refuse to answer",
                    "I am just a language model"]
    gemini.set_default_response('refused')
    for answer in punt_answers:
        lmanswer = LMAnswer(answer=answer, raw_response=answer,
                            generation_time=0.0, model=gemini)
        score = punt_detector.score(lmanswer, question, task=None)
        print(punt_answers)
        assert score == 1.0
