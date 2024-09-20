import os
from lmeval.models.ollama import OllamaModel
from lmeval import get_scorer, ScorerType, Question, Task, TaskType
from lmeval import Category
from lmeval.evaluator import Evaluator, EvalTask
from lmeval.prompts import SingleWordAnswerPrompt
from .tests_utils import eval_single_text_generation, eval_batch_text_generation, eval_image_analysis

def test_ollama_single_text_generation():
    eval_single_text_generation(OllamaModel())

def test_ollama_batch_text_generation():
    eval_batch_text_generation(OllamaModel())

# def test_openai_image_analysis():
#     eval_image_analysis(OpenAIModel())
