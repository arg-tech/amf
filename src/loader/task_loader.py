from src.argument_relation.predictor import ArgumentRelationPredictor
from src.turninator.turninator import Turninator
from src.segmenter.segmenter import Segmenter
from src.propositionaliser.propositionalizer import Propositionalizer

class Task:
    def __init__(self, task_type, model_name = None, variant = None):
        self.task_type = task_type
        self.model_name = model_name
        self.variant = variant

    def get_task(self):
        if self.task_type == "argument_relation":
            return ArgumentRelationPredictor(self.model_name, self.variant)
        elif self.task_type == "turninator":
            return Turninator
        elif self.task_type == "segmenter":
            return Segmenter
        elif self.task_type == "propositionalizer":
            return Propositionalizer
        else:
            raise ValueError(f"Unknown task type: {self.task_type}")
def load_amf_component(task_name, *args):
    """Initialize a component using the Task."""
    return Task(task_name, *args).get_task()

