import pytest
from .fixtures import gemini

def test_gemini_fixture(gemini):

    # check our model is working
    answer = gemini.generate_text('Say hello in french!')
    assert 'bonjour' in answer.answer.lower()
    assert not answer.iserror
    assert not answer.error_reason
    assert not answer.ispunting
    assert not answer.punting_reason
    assert answer.steps[0].execution_time > 0.1
    assert answer.score == 0.0  # no scoring yet
    assert 'gemini' in answer.model.name.lower()
    assert 'gemini' in answer.model.version_string.lower()
