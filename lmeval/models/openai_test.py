import os
from lmeval.models.openai import OpenAIModel
from lmeval import get_scorer, ScorerType, Question, Task, TaskType
from lmeval import Category
from lmeval.evaluator import Evaluator, EvalTask
from lmeval.prompts import SingleWordAnswerPrompt
from .tests_utils import eval_single_text_generation, eval_batch_text_generation, eval_image_analysis

def test_openai_single_text_generation():
    eval_single_text_generation(OpenAIModel())

def test_openai_batch_text_generation():
    eval_batch_text_generation(OpenAIModel())

def test_openai_image_analysis():
    eval_image_analysis(OpenAIModel())
