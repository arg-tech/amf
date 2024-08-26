from amf.argument_relation.predictor import ArgumentRelationPredictor
from amf.hypothesis.predictor import HypothesisPredictor
from amf.scheme.predictor import SchemePredictor
from amf.turninator.turninator import Turninator
from amf.segmenter.segmenter import Segmenter
from amf.propositionaliser.propositionalizer import Propositionalizer
from amf.utils.visualise import JsonToSvgConverter

class Module:
    def __init__(self, task_type, model_name=None, variant=None):
        """
        Initialize the Task class with the appropriate component based on task_type.

        Args:
            task_type (str): The type of task to load.
            model_name (str, optional): The model name if required by the component.
            variant (str, optional): The variant if required by the component.
        """
        self.task_type = task_type
        self.model_name = model_name
        self.variant = variant
        self.component = self._initialize_component()

    def _initialize_component(self):
        """Private method to initialize the appropriate component based on task_type."""
        if self.task_type == "argument_relation":
            return ArgumentRelationPredictor(self.model_name, self.variant)
        elif self.task_type == "turninator":
            return Turninator()
        elif self.task_type == "segmenter":
            return Segmenter()
        elif self.task_type == "propositionalizer":
            return Propositionalizer()
        elif self.task_type == "hypothesis": 
            return HypothesisPredictor(self.model_name, self.variant)
        elif self.task_type == "scheme":         
            return SchemePredictor(self.model_name, self.variant)
        
        elif self.task_type == "visualiser":
            return JsonToSvgConverter()
        else:
            raise ValueError(f"Unknown task type: {self.task_type}")

    def __getattr__(self, name):
        """Delegate attribute access to the loaded component."""
        return getattr(self.component, name)

    def __call__(self, *args, **kwargs):
        """Allow the Task object to be called directly if the component is callable."""
        return self.component(*args, **kwargs)
