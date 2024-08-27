"""Module for predicting argument relations and processing XAIF structures."""

import json
import os
import logging
from .model import Classifier
from argument_mining_framework.utils.data_utils import Data

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HypothesisPredictor:
    """
    A class for predicting argument relations and processing XAIF structures.

    Attributes:
        pipe: The model pipeline for predictions.
        tokenizer: The tokenizer associated with the model.
        data: An instance of the Data class for data processing.

    Methods:
        __init__(model_type: str, variant: str): Initializes the predictor with the specified model.
        predict(data): Runs predictions on the input data in batches.
        argument_map(x_aif: str): Processes XAIF structure and generates argument mappings.
        _update_aif_structure(aif, refined_structure): Updates the AIF structure with predicted relations.
    """

    def __init__(self, model_type: str, variant: str):
        """
        Initializes the predictor by loading the appropriate model based on config.

        Args:
            model_type (str): Type of the model (e.g., 'dialogpt', 'roberta').
            variant (str): Variant of the model (e.g., 'vanila').
        """
        try:
            # Get the directory of the current script
            script_dir = os.path.dirname(__file__)
            config_path = os.path.join(script_dir, 'config.json')

            with open(config_path, 'r') as f:
                config = json.load(f)
            assert model_type in config, f"Model type '{model_type}' not found in config."
            assert variant in config[model_type], f"Variant '{variant}' not found for model type '{model_type}'."

            model_name = config[model_type][variant]
            self.pipe, self.tokenizer = Classifier(model_name)
            self.data = Data() 
            logger.info(f"Successfully loaded model: {model_name}")

        except FileNotFoundError as e:
            logger.error(f"Config file not found: {e}")
            raise
        except AssertionError as e:
            logger.error(f"Invalid model or variant: {e}")
            raise
        except Exception as e:
            logger.error(f"An error occurred during initialization: {e}")
            raise

    def predict(self, raw_data):
        """
        Runs predictions on the input data in batches.

        Args:
            data: Input data for prediction.

        Returns:
            Tuple: (predictions, confidence, probabilities)
                - predictions (list): List of predicted labels.
                - confidence (list): List of confidence scores for the predictions.
                - probabilities (list): List of probability scores for the predictions.
        """
        try:
            input_data, _ = self.data.load_data(raw_data, "hypothesis")
            
            predictions, confidence, probabilities = [], [], []
            batch_size = 64

            for start_idx in range(0, len(input_data), batch_size):
                batch_data = input_data[start_idx:start_idx + batch_size]
                label_cores_batch = self.pipe(batch_data)

                for label_core in label_cores_batch:
                    predictions.append(label_core['label'])
                    confidence.append(label_core['score'])
                    probabilities.append(label_core['score'])

            return predictions, confidence, probabilities

        except Exception as e:
            logger.error(f"Error during prediction: {e}")
            raise


