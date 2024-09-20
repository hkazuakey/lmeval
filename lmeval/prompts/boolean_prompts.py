from .prompt import Prompt
from ..enums import TaskType

class TrueOrFalseAnswerPrompt(Prompt):
    def __init__(self,
                template: str = """Accurately answer by true or false the following question "{{question.question}}" """,
                name: str = "True or False Answer",
                description: str = "Ask the model to answer the question by true or false",
                task_type = TaskType.boolean,
                url: str = '',
                version: str = '1.0'):

        super().__init__(name=name, description=description,
                        task_type=task_type, template=template, url=url,
                        version=version)
