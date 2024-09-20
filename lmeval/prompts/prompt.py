from ..template_engine import TemplateEngine
from ..custom_model import CustomModel
from ..enums import TaskType
from ..question import Question
from ..task import Task

class Prompt(CustomModel):
    name: str
    description: str
    url: str  # if from public source

    task_type: TaskType
    template: str  # the template to use for this prompt
    version: str

    def __str__(self) -> str:
        # use name and version for unique identification in the benchmark data
        return str(f"{self.name}")

    def version_string(self) -> str:
        "Return prompt versioned name"
        return f"{self.name}-{self.version}".replace(' ', '_').lower()

    def render(self, question: Question, task: Task) -> str:
        "Render prompt for a given question and task"

        if task.type != self.task_type:
            raise ValueError(f"Task type {task.type} does not match prompt task type {self.task_type}")
        template = TemplateEngine(self.template)
        return template.render(question=question, task=task)