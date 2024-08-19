import json
import logging
from itertools import combinations
from .model import Loader
from .output import Output
from .utils import Data
from xaif_eval import xaif

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ArgumentRelationPredictor:
    """Predictor class for handling model loading, predictions, and argument mapping."""

    def __init__(self, model_type: str, variant: str):
        """
        Initializes the Predictor by loading the appropriate model based on config.

        Args:
            model_type (str): Type of the model (e.g., 'dialogpt', 'roberta').
            variant (str): Variant of the model (e.g., 'vanila').
        """
        try:
            with open('argumentminingnlp/argumentminingnlp/argument_relation_prediction/config.json', 'r') as f:
                config = json.load(f)
            assert model_type in config, f"Model type '{model_type}' not found in config."
            assert variant in config[model_type], f"Variant '{variant}' not found for model type '{model_type}'."

            model_name = config[model_type][variant]
            self.pipe, self.tokenizer = Loader(model_name).load_model()
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

    def predict(self, data):
        """
        Runs predictions on the input data in batches.

        Args:
            data: Input data for prediction.

        Returns:
            Tuple of (predictions, confidence, probabilities).
        """
        try:
            input_data = self.data.prepare_inputs(data, context=False)
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

    def argument_map(self, x_aif: str):
        """
        Processes the XAIF structure and generates argument mappings.

        Args:
            x_aif (str): Input XAIF structure as a JSON string.

        Returns:
            Modified XAIF structure with predicted relations.
        """
        try:
            # Parse input JSON and build the AIF structure
            x_aif = json.loads(x_aif)
            aif = xaif.AIF(x_aif)

            # Load node data for argument prediction
            data, combined_texts = self.data.load_data(aif.aif.get('nodes'))
            predictions, confidence, _ = self.predict(data)
            logger.info(f"Predictions: {predictions}")

            predicted_relations, propositions = [], []

            for (p1, p2), relation in zip(combined_texts, predictions):
                if relation in ["CA", "RA", "MA"]:
                    predicted_relations.append((p1, p2, relation))
                    if p1 not in propositions:
                        propositions.append(p1)
                    if p2 not in propositions:
                        propositions.append(p2)

            # Format and refine the output structure
            outputs = Output()
            refined_structure = outputs.format(propositions, predicted_relations, remove_indirect_edges=True)
            logger.info(f"Refined structure: {refined_structure}")

            # Update the AIF structure based on predicted relations
            self._update_aif_structure(aif, refined_structure)

            return aif.xaif

        except json.JSONDecodeError as e:
            logger.error(f"Invalid XAIF JSON format: {e}")
            raise
        except Exception as e:
            logger.error(f"Error during argument mapping: {e}")
            raise

    def _update_aif_structure(self, aif, refined_structure):
        """
        Updates the AIF structure with predicted argument relations.

        Args:
            aif: The AIF object.
            refined_structure: The refined argument structure.

        Returns:
            None
        """
        try:
            for conclusion_id, premise_relation_list in refined_structure.items():
                premises = premise_relation_list[:len(premise_relation_list)//2]
                relations = premise_relation_list[len(premise_relation_list)//2:]

                for premise_id, ar_type in zip(premises, relations):
                    if ar_type in ['CA', 'RA', 'MA']:
                        logger.info(f"Adding {ar_type} relation between {conclusion_id} and {premise_id}")
                        aif.add_component("argument_relation", ar_type, conclusion_id, premise_id)

        except Exception as e:
            logger.error(f"Error updating AIF structure: {e}")
            raise
