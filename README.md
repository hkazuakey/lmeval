# LMEval: Large Model Evaluation Framework

## Installation

```bash
pip install lmeval
```

### Dev setup

LMeval use `uv` that you need to install then

```bash
uv venv
source .venv/bin/activate  # or open a new term in vscode after accepting the new venv
uv pip compile --all-extras pyproject.toml > requirements.txt
uv pip install -r requirements.txt
```

### How to use a custom template / custom prompt?

Import any standard prompt that match the type of task you want to perform and simply
supply at least the `name` and `template` arguments. Supplying a custom name,
and potentially `version` is mandatory as the benchmark track performance for
each `prompt/version` so otherwise your results will be clamped.

```python
from lmeval.prompts import QuestionOnlyPrompt

prompt = QuestionOnlyPrompt(name="mycustom prompt",
                            template="""
                            This is a custom prompt:
                             - question: {{question.question}}
                             - answer: {{question.answer}}
                            """"
```

## Disclaimer

This is not a Google product.