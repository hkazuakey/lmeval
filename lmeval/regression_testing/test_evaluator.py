# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from dotenv import load_dotenv
from lmeval.models.gemini import GeminiModel
from lmeval import Question, Task, TaskType, Category
from lmeval import get_scorer, ScorerType
from lmeval.prompts import Prompt, SingleWordAnswerPrompt
from lmeval.evaluator import Evaluator, EvalTask
from .fixtures import gemini

def test_evalute_question(gemini):
    prompt = SingleWordAnswerPrompt()
    scorer = get_scorer(ScorerType.always_1)

    category_name = 'eu'
    category = Category(name=category_name, description='European geography questions')
    task = Task(name="This is a test task.", type=TaskType.text_generation,
                scorer=scorer)
    question = Question(id=1, question="what is the capital of France?", answer="Paris")

    task = EvalTask(benchmark_name='Test',
                    task=task,
                    category=category,
                    question=question,
                    prompt=prompt,
                    lm_model=gemini)

    task = Evaluator.generate_answer(task)
    task = Evaluator.score_answer(task)
    assert task.score == 1.0
    assert not task.punted
    assert "paris" in task.lm_answer.answer.lower()
