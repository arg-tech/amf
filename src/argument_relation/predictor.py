"""Module for predicting argument relations and processing XAIF structures."""

import json
import os
import logging
from xaif_eval import xaif
from utils.output import ArgumentRelationOutput
from utils.data_utils import Data
from .model import Loader

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ArgumentRelationPredictor:
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
            self.pipe, self.tokenizer = Loader(model_name).load_model()
            self.data = Data()
            logger.info("Successfully loaded model: %s", model_name)

        except FileNotFoundError as e:
            logger.error("Config file not found: %s", e)
            raise
        except AssertionError as e:
            logger.error("Invalid model or variant: %s", e)
            raise
        except Exception as e:
            logger.error("An error occurred during initialization: %s", e)
            raise

    def predict(self, data):
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
            logger.error("Error during prediction: %s", e)
            raise

    def get_argument_map(self, x_aif: str):
        """
        Processes the XAIF structure and generates argument mappings.

        Args:
            x_aif (str): Input XAIF structure as a JSON string.

        Returns:
            dict: Modified XAIF structure with predicted relations.
        """
        try:
            # Parse input JSON and build the AIF structure
            #x_aif = json.loads(x_aif)
            aif = xaif.AIF(x_aif)

            # Load node data for argument prediction
            data, combined_texts = self.data.load_data(aif.aif.get('nodes'))
            predictions, _, _ = self.predict(data)
            logger.info("Predictions: %s", predictions)

            predicted_relations, propositions = [], []

            for (p1, p2), relation in zip(combined_texts, predictions):
                if relation in ["CA", "RA", "MA"]:
                    predicted_relations.append((p1, p2, relation))
                    if p1 not in propositions:
                        propositions.append(p1)
                    if p2 not in propositions:
                        propositions.append(p2)

            # Format and refine the output structure
            outputs = ArgumentRelationOutput()
            refined_structure = outputs.format(propositions, predicted_relations, remove_indirect_edges=True)
            logger.info("Refined structure: %s", refined_structure)

            # Update the AIF structure based on predicted relations
            self._update_aif_structure(aif, refined_structure)

            return aif.xaif

        except json.JSONDecodeError as e:
            logger.error("Invalid XAIF JSON format: %s", e)
            raise
        except Exception as e:
            logger.error("Error during argument mapping: %s", e)
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
                premises = premise_relation_list[:len(premise_relation_list) // 2]
                relations = premise_relation_list[len(premise_relation_list) // 2:]

                for premise_id, ar_type in zip(premises, relations):
                    if ar_type in ['CA', 'RA', 'MA']:
                        logger.info(f"Adding {ar_type} relation between {conclusion_id} and {premise_id}")
                        aif.add_component("argument_relation", ar_type, conclusion_id, premise_id)

        except Exception as e:
            logger.error("Error updating AIF structure: %s",  e)
    def get_all_claims(self, xaif_input):
        return self._extract_claims_and_evidence(xaif_input).keys()

    def get_evidence_for_claim(self, claim, xaif_input):
        claims_and_evidence = self._extract_claims_and_evidence(xaif_input)
        if claim in claims_and_evidence:
            return claims_and_evidence[claim]
        return f'No evidence found for the specified claim: {claim}'

    def _extract_claims_and_evidence(self, xaif_input):
        ARNodes = {node['nodeID']:node['text'] for node in xaif_input['AIF']['nodes'] if node['type'] in ['CA', 'RA', "MA"]}
        INodes = {node['nodeID']:node['text'] for node in xaif_input['AIF']['nodes'] if node['type'] in ['I']}
        claims_supports = {}
        for edge in xaif_input['AIF']['edges']:
            if edge['fromID'] in ARNodes.keys():
                ARNodeID = edge['fromID']
                if edge['toID'] in INodes.keys():
                    claimNodeID = edge['toID']
                    for edge2 in xaif_input['AIF']['edges']:
                        if edge2['toID'] == ARNodeID and  edge2['toID'] in ARNodes.keys():
                            if edge2['fromID'] in  INodes.keys():
                                supportNodeID = edge2['fromID']
                                if claimNodeID in claims_supports:
                                    if supportNodeID not in claims_supports[claimNodeID]:
                                        claims_supports[claimNodeID].append(supportNodeID)
                                else:
                                    claims_supports[claimNodeID] = [supportNodeID]

        for edge in xaif_input['AIF']['edges']:
            if edge['toID'] in ARNodes.keys():
                ARNodeID = edge['toID']
                if edge['fromID'] in INodes.keys():
                    supportNodeID = edge['fromID']                    
                    for edge2 in xaif_input['AIF']['edges']:
                        if edge2['fromID'] == ARNodeID and  edge2['fromID'] in ARNodes.keys():
                            if edge2['toID'] in  INodes.keys():
                                claimNodeID = edge2['toID']
                                if claimNodeID in claims_supports:
                                    if supportNodeID not in claims_supports[claimNodeID]:
                                        claims_supports[claimNodeID].append(supportNodeID)
                                else:
                                    claims_supports[claimNodeID] = [supportNodeID]
        return  ({INodes[claimID]: [INodes[evidenceID] for evidenceID in list_evidences_id] 
                  for claimID, list_evidences_id in claims_supports.items()})