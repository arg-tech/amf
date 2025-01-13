import importlib
import logging

# Custom exceptions
class ModuleInitializationError(Exception):
    pass

class ComponentNotFoundError(ModuleInitializationError):
    pass

class ComponentClassNotFoundError(ModuleInitializationError):
    pass

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Module:
    """
    A class to dynamically load and manage components based on task_type.

    Attributes:
        task_type (str): The type of task to load.
        model_name (str, optional): The model name if required by the component.
        variant (str, optional): The variant if required by the component.
        component: The loaded component based on the task type.
    """

    # Dictionary to map task types to module paths and class names
    COMPONENT_MAP = {
        "argument_relation": ('argument_relation.predictor', 'ArgumentRelationPredictor'),
        "turninator": ('turninator.turninator', 'Turninator'),
        "segmenter": ('segmenter.segmenter', 'Segmenter'),
        "propositionalizer": ('propositionaliser.propositionalizer', 'Propositionalizer'),
        "hypothesis": ('hypothesis.predictor', 'HypothesisPredictor'),
        "scheme": ('scheme.predictor', 'SchemePredictor'),
        "visualiser": ('utils.visualise', 'JsonToSvgConverter')
        
    }

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
        try:
            module_path, class_name = self._get_component_info(self.task_type)
            return self._load_component(module_path, class_name)
        except (KeyError, ValueError) as e:
            logger.error(f"Failed to initialize component for task_type '{self.task_type}': {e}")
            raise ModuleInitializationError(f"Error initializing component: {e}")

    def _get_component_info(self, task_type):
        """Get the module path and class name for the given task_type."""
        if task_type not in self.COMPONENT_MAP:
            raise ValueError(f"Unknown task type: {task_type}")
        return self.COMPONENT_MAP[task_type]

    def _load_component(self, module_path, class_name):
        """Dynamically load the specified component class."""
        try:
            module = importlib.import_module(f'argument_mining_framework.{module_path}')
            component_class = getattr(module, class_name)
            if class_name in ["Turninator", "Segmenter", "JsonToSvgConverter", "Propositionalizer"]:  # Components that do not require additional arguments
                return component_class()
            else:
                return component_class(self.model_name, self.variant)
        except ImportError:
            logger.error(f"Module '{module_path}' could not be imported.")
            raise ComponentNotFoundError(f"Module '{module_path}' not found.")
        except AttributeError:
            logger.error(f"Component class '{class_name}' not found in module '{module_path}'.")
            raise ComponentClassNotFoundError(f"Component class '{class_name}' not found in module '{module_path}'.")

    def __getattr__(self, name):
        """Delegate attribute access to the loaded component."""
        return getattr(self.component, name)

    def __call__(self, *args, **kwargs):
        """Allow the Task object to be called directly if the component is callable."""
        return self.component(*args, **kwargs)
