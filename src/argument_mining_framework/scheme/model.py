"""
Module for loading and using a text classification model.
"""

from transformers import AutoTokenizer, pipeline

class Classifier:
    """
    Loads a text classification model and tokenizer.

    Attributes:
        model_name (str): The name of the model to load.
        classifier: The text classification pipeline.
        tokenizer: The tokenizer for the model.
    """

    def __init__(self, model_name: str):
        """
        Initialize with the specified model name and load the model.

        Args:
            model_name (str): The name of the model to load.
        """
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.classifier = pipeline("text-classification", model=self.model_name, tokenizer=self.tokenizer)

    def __iter__(self):
        """Allow unpacking of classifier and tokenizer."""
        return iter((self.classifier, self.tokenizer))
