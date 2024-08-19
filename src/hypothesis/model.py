"""Module for loading and using a text classification model."""

from transformers import AutoTokenizer, pipeline

class Loader:
    """
    Loader class for loading a text classification model and tokenizer.

    Attributes:
        model_name (str): The name of the model to be loaded.
    """

    def __init__(self, model_name: str):
        """
        Initialize the Loader with the given model name.

        Args:
            model_name (str): The name of the model to be loaded.
        """
        self.model_name = model_name

    def load_model(self):
        """
        Load the model and tokenizer into a pipeline.

        Returns:
            tuple: A tuple containing the classifier pipeline and tokenizer.
        """
        tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        classifier = pipeline("text-classification", model=self.model_name, tokenizer=tokenizer)
        return classifier, tokenizer
