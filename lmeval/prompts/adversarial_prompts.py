from .prompt import Prompt
from ..enums import TaskType

class AdversarialChainOfThoughtsPrompt(Prompt):
    def __init__(self,
                template: str = "{{question.question}} Let's think step by step and answer the question starting with Answer:",
                name: str = "Adversarial Chain of Thoutghts",
                description: str = "Ask the model to think steps by steps before answering the question",
                task_type = TaskType.text_generation,
                url: str = '',
                version: str = '1.0'):

        super().__init__(name=name, description=description,
                        task_type=task_type, template=template, url=url,
                        version=version)
