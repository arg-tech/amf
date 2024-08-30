"""Module for predicting argument relations and processing XAIF structures."""

import json
import os
import logging
from xaif_eval import xaif
from argument_mining_framework.utils.output import ArgumentRelationOutput
from argument_mining_framework.utils.data_utils import Data
from .sequence_classifier.model import Classifier

from .dam.ArgumentRelationAnalyser.dam1_features_map import Dam1ArgumentRelationAnalyzer
from .dam.ArgumentRelationAnalyser.dam2_features_map import Dam2ArgumentRelationAnalyzer
from .dam.ArgumentRelationAnalyser.dam3_features_map import Dam3ArgumentRelationAnalyzer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ArgumentRelationAnalyzerFactory:
    """Factory to create instances of argument relation analyzers based on DAM versions."""
    
    _analyzers = {
        "01": Dam1ArgumentRelationAnalyzer,
        "02": Dam2ArgumentRelationAnalyzer,
        "03": Dam3ArgumentRelationAnalyzer
    }

    @classmethod
    def get_analyzer(cls, dam_version):
        """Returns the appropriate analyzer based on the dam_version."""
        if dam_version in cls._analyzers:
            return cls._analyzers[dam_version]()
        raise ValueError(f"Unsupported DAM version: {dam_version}")

class DAMPredictor:
    """Predictor for handling argument relations using the DAM framework."""
    
    def __init__(self, dam_version: str):
        """Initialize the predictor with the specified DAM version."""
        self.analyzer = ArgumentRelationAnalyzerFactory.get_analyzer(dam_version)

    def get_argument_map(self, x_aif: str) -> dict:
        """Retrieve the argument structure from the input data."""
        xaif_obj = xaif.AIF(x_aif)
        propositions_id_pairs = self._get_propositions_id_pairs(xaif_obj.aif)
        self._update_node_edges_with_relations(propositions_id_pairs, xaif_obj)
        return xaif_obj.xaif

    def _get_propositions_id_pairs(self, aif: dict) -> dict:
        """Extract proposition ID pairs from the AIF data."""
        propositions_id_pairs = {}
        for node in aif.get('nodes', []):
            if node.get('type') == "I":
                proposition = node.get('text', '').strip()
                if proposition:
                    node_id = node.get('nodeID')
                    propositions_id_pairs[node_id] = proposition
        return propositions_id_pairs

    def _update_node_edges_with_relations(self, propositions_id_pairs: dict, xaif_obj: xaif.AIF):
        """Update the nodes and edges in the AIF structure to reflect new relations."""
        checked_pairs = set()
        for prop1_node_id, prop1 in propositions_id_pairs.items():
            for prop2_node_id, prop2 in propositions_id_pairs.items():
                if prop1_node_id != prop2_node_id:
                    pair = frozenset([prop1_node_id, prop2_node_id])
                    if pair not in checked_pairs:
                        checked_pairs.add(pair)
                        prediction = self.analyzer.get_argument_relation((prop1, prop2))
                        if prediction in ['RA', 'MA', 'CA']:
                            xaif_obj.add_component("argument_relation", prediction, prop1_node_id, prop2_node_id)

    def get_all_claims(self, xaif_input: dict):
        """Return all claims from the XAIF input."""
        return self._extract_claims_and_evidence(xaif_input).keys()

    def get_evidence_for_claim(self, claim: str, xaif_input: dict):
        """Return the evidence supporting a specific claim."""
        claims_and_evidence = self._extract_claims_and_evidence(xaif_input)
        return claims_and_evidence.get(claim, f'No evidence found for the specified claim: {claim}')

    def _extract_claims_and_evidence(self, xaif_input: dict) -> dict:
        """Extracts claims and supporting evidence from the given XAIF input."""
        ar_nodes = {node['nodeID']: node['text'] for node in xaif_input['AIF']['nodes'] if node['type'] in ['CA', 'RA', 'MA']}
        i_nodes = {node['nodeID']: node['text'] for node in xaif_input['AIF']['nodes'] if node['type'] == 'I'}
        claims_supports = {}

        for edge in xaif_input['AIF']['edges']:
            ar_node_id = edge.get('fromID')
            claim_node_id = edge.get('toID')

            if ar_node_id in ar_nodes and claim_node_id in i_nodes:
                for support_edge in xaif_input['AIF']['edges']:
                    support_node_id = support_edge.get('fromID')
                    if support_edge.get('toID') == ar_node_id and support_node_id in i_nodes:
                        claims_supports.setdefault(claim_node_id, []).append(support_node_id)

        for edge in xaif_input['AIF']['edges']:
            support_node_id = edge.get('fromID')
            ar_node_id = edge.get('toID')

            if support_node_id in i_nodes and ar_node_id in ar_nodes:
                for claim_edge in xaif_input['AIF']['edges']:
                    claim_node_id = claim_edge.get('toID')
                    if claim_edge.get('fromID') == ar_node_id and claim_node_id in i_nodes:
                        claims_supports.setdefault(claim_node_id, []).append(support_node_id)

        return {i_nodes[claim_id]: [i_nodes[evidence_id] for evidence_id in evidence_ids]
                for claim_id, evidence_ids in claims_supports.items()}


class PipelinePredictor:
    """A class for predicting argument relations and processing XAIF structures using a model pipeline."""

    def __init__(self, model_type: str, variant: str):
        """Initialize the predictor by loading the appropriate model based on config."""
        self.pipe, self.tokenizer = self._load_model(model_type, variant)
        self.data = Data()

    def _load_model(self, model_type: str, variant: str):
        """Load model pipeline and tokenizer from configuration."""
        try:
            config_path = os.path.join(os.path.dirname(__file__), 'sequence_classifier/config.json')
            with open(config_path, 'r') as f:
                config = json.load(f)

            assert model_type in config, f"Model type '{model_type}' not found in config."
            assert variant in config[model_type], f"Variant '{variant}' not found for model type '{model_type}'."

            model_name = config[model_type][variant]
            logger.info("Successfully loaded model: %s", model_name)
            return Classifier(model_name)
        except FileNotFoundError as e:
            logger.error("Config file not found: %s", e)
            raise
        except AssertionError as e:
            logger.error("Invalid model or variant: %s", e)
            raise
        except Exception as e:
            logger.error("An error occurred during model loading: %s", e)
            raise

    def predict(self, data):
        """Run predictions on the input data in batches."""
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
        """Processes the XAIF structure and generates argument mappings."""
        try:
            aif = xaif.AIF(x_aif)
            data, combined_texts = self.data.load_data(aif.aif.get('nodes'), "argument_relation")
            predictions, _, _ = self.predict(data)
            predicted_relations, propositions = self._extract_relations(combined_texts, predictions)
            refined_structure = ArgumentRelationOutput().format(propositions, predicted_relations, remove_indirect_edges=True)
            self._update_aif_structure(aif, refined_structure)
            return aif.xaif

        except json.JSONDecodeError as e:
            logger.error("Invalid XAIF JSON format: %s", e)
            raise
        except Exception as e:
            logger.error("Error during argument mapping: %s", e)
            raise

    def _extract_relations(self, combined_texts, predictions):
        """Extract and format predicted relations."""
        predicted_relations, propositions = [], []
        for (p1, p2), relation in zip(combined_texts, predictions):
            if relation in ["CA", "RA", "MA"]:
                predicted_relations.append((p1, p2, relation))
                if p1 not in propositions:
                    propositions.append(p1)
                if p2 not in propositions:
                    propositions.append(p2)
        return predicted_relations, propositions

    def _update_aif_structure(self, aif, refined_structure):
        """Update the AIF structure with predicted argument relations."""
        try:
            for conclusion_id, premise_relation_list in refined_structure.items():
                premises = premise_relation_list[:len(premise_relation_list) // 2]
                relations = premise_relation_list[len(premise_relation_list) // 2:]
                for premise_id, ar_type in zip(premises, relations):
                    if ar_type in ['CA', 'RA', 'MA']:
                        logger.info(f"Adding {ar_type} relation between {conclusion_id} and {premise_id}")
                        aif.add_component("argument_relation", ar_type, conclusion_id, premise_id)
        except Exception as e:
            logger.error("Error updating AIF structure: %s", e)
    def get_all_claims(self, xaif_input):
        return self._extract_claims_and_evidence(xaif_input).keys()

    def get_evidence_for_claim(self, claim, xaif_input):
        claims_and_evidence = self._extract_claims_and_evidence(xaif_input)
        if claim in claims_and_evidence:
            return claims_and_evidence[claim]
        return f'No evidence found for the specified claim: {claim}'
    
    def _extract_claims_and_evidence(self, xaif_input):
        """Extracts claims and supporting evidence from the given XAIF input."""

        # Separate AR nodes (claims) and I nodes (evidence)
        ar_nodes = {node['nodeID']: node['text'] for node in xaif_input['AIF']['nodes'] if node['type'] in ['CA', 'RA', 'MA']}
        i_nodes = {node['nodeID']: node['text'] for node in xaif_input['AIF']['nodes'] if node['type'] == 'I'}

        claims_supports = {}

        # Process edges to map claims to their supporting evidence
        for edge in xaif_input['AIF']['edges']:
            ar_node_id = edge.get('fromID')
            claim_node_id = edge.get('toID')

            if ar_node_id in ar_nodes and claim_node_id in i_nodes:
                # Look for evidence nodes linked to the AR node
                for support_edge in xaif_input['AIF']['edges']:
                    support_node_id = support_edge.get('fromID')

                    if support_edge.get('toID') == ar_node_id and support_node_id in i_nodes:
                        if claim_node_id not in claims_supports:
                            claims_supports[claim_node_id] = []
                        if support_node_id not in claims_supports[claim_node_id]:
                            claims_supports[claim_node_id].append(support_node_id)

        # Reverse mapping: evidence pointing to claims
        for edge in xaif_input['AIF']['edges']:
            support_node_id = edge.get('fromID')
            ar_node_id = edge.get('toID')

            if support_node_id in i_nodes and ar_node_id in ar_nodes:
                for claim_edge in xaif_input['AIF']['edges']:
                    claim_node_id = claim_edge.get('toID')

                    if claim_edge.get('fromID') == ar_node_id and claim_node_id in i_nodes:
                        if claim_node_id not in claims_supports:
                            claims_supports[claim_node_id] = []
                        if support_node_id not in claims_supports[claim_node_id]:
                            claims_supports[claim_node_id].append(support_node_id)

        # Create final dictionary mapping claims to their supporting evidence texts
        claims_evidence = {
            i_nodes[claim_id]: [i_nodes[evidence_id] for evidence_id in evidence_ids]
            for claim_id, evidence_ids in claims_supports.items()
        }

        return claims_evidence
    
class ArgumentRelationPredictor:
    """Facade for predicting argument relations using either DAM or pipeline models."""
    
    def __init__(self, model_type: str, variant: str = None):
        """
        Initialize the ArgumentRelationPredictor with the appropriate predictor based on model_type.
        
        Args:
            model_type (str): Type of the model (e.g., 'DAM', 'dialogpt').
            variant (str): Optional variant for the model (e.g., 'vanilla') if model_type is DAM.
        """
        if model_type == "DAM":
            if variant is None:
                raise ValueError("DAM model requires a variant.")
            self.predictor = DAMPredictor(dam_version=variant)
        else:
            self.predictor = PipelinePredictor(model_type, variant)

    def get_argument_map(self, x_aif: str) -> dict:
        """Retrieve the argument structure from the input data."""
        return self.predictor.get_argument_map(x_aif)

    def get_all_claims(self, xaif_input: dict):
        """Get all claims from the XAIF input."""
        return self.predictor.get_all_claims(xaif_input)

    def get_evidence_for_claim(self, claim: str, xaif_input: dict):
        """Get evidence for a specific claim."""
        return self.predictor.get_evidence_for_claim(claim, xaif_input)
