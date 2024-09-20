from .gemini import GeminiModel
from .tests_utils import eval_single_text_generation, eval_batch_text_generation, eval_image_analysis


def test_gemini_single_text_generation():
    eval_single_text_generation(GeminiModel())

def test_gemini_batch_text_generation():
    eval_batch_text_generation(GeminiModel())

def test_gemini_image_analysis():
    eval_image_analysis(GeminiModel())
