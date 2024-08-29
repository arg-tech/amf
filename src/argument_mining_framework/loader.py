import importlib

class Module:
    def __init__(self, task_type, model_name=None, variant=None):
        """
        Initialize the Module class with the appropriate component based on task_type.

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
            return self._load_component('argument_relation.predictor', 'ArgumentRelationPredictor')
        elif self.task_type == "turninator":
            return self._load_component('turninator.turninator', 'Turninator')
        elif self.task_type == "segmenter":
            return self._load_component('segmenter.segmenter', 'Segmenter')
        elif self.task_type == "propositionalizer":
            return self._load_component('propositionaliser.propositionalizer', 'Propositionalizer')
        elif self.task_type == "hypothesis":
            return self._load_component('hypothesis.predictor', 'HypothesisPredictor')
        elif self.task_type == "scheme":
            return self._load_component('scheme.predictor', 'SchemePredictor')
        elif self.task_type == "visualiser":
            return self._load_component('utils.visualise', 'JsonToSvgConverter')
        else:
            raise ValueError(f"Unknown task type: {self.task_type}")

    def _load_component(self, module_path, class_name):
        """Dynamically load the specified component class."""
        try:
            module = importlib.import_module(f'argument_mining_framework.{module_path}')
            component_class = getattr(module, class_name)
            if class_name in ["Turninator", "Segmenter", "visualiser", "Propositionalizer", "JsonToSvgConverter"]:  # Components that do not require additional arguments
                return component_class()
            else:
                return component_class(self.model_name, self.variant)
        except ImportError:
            raise RuntimeError(f"Module or component '{module_path}.{class_name}' not found.")
        except AttributeError:
            raise RuntimeError(f"Component class '{class_name}' not found in module '{module_path}'.")

    def __getattr__(self, name):
        """Delegate attribute access to the loaded component."""
        return getattr(self.component, name)

    def __call__(self, *args, **kwargs):
        """Allow the Task object to be called directly if the component is callable."""
        return self.component(*args, **kwargs)
