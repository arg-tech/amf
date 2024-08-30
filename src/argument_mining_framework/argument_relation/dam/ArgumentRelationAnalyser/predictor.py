from xaif_eval import xaif
from .dam1_features_map import Dam1ArgumentRelationAnalyzer
from .dam2_features_map import Dam2ArgumentRelationAnalyzer
from .dam3_features_map import Dam3ArgumentRelationAnalyzer



class Predictor:
    def __init__(self,dam_verssion):
        if dam_verssion == "1":
            self.DamArgumentRelationAnalyzer = Dam1ArgumentRelationAnalyzer()
        if dam_verssion == "2":
            self.DamArgumentRelationAnalyzer = Dam2ArgumentRelationAnalyzer()
        if dam_verssion == "3":
            self.DamArgumentRelationAnalyzer = Dam3ArgumentRelationAnalyzer()
    
    def get_argument_structure(self,x_aif):
        """Retrieve the argument structure from the input data."""

        # Parse input JSON and build the AIF structure
        #x_aif = json.loads(x_aif)
        xaif_obj = xaif.AIF(x_aif)

        # Load node data for argument prediction
        #data, combined_texts = self.data.load_data(aif.aif.get('nodes'),"argument_relation")
        propositions_id_pairs = self.get_propositions_id_pairs(xaif_obj.aif)
        self.update_node_edge_with_relations(propositions_id_pairs, xaif_obj)
        return xaif_obj.xaif
    


    def get_propositions_id_pairs(self, aif):
        """Extract proposition ID pairs from the AIF data."""
        propositions_id_pairs = {}
        for node in aif.get('nodes', []):
            if node.get('type') == "I":
                proposition = node.get('text', '').strip()
                if proposition:
                    node_id = node.get('nodeID')
                    propositions_id_pairs[node_id] = proposition
        return propositions_id_pairs
    
    def update_node_edge_with_relations(self, propositions_id_pairs, xaif_obj):
        """
        Update the nodes and edges in the AIF structure to reflect the new relations between propositions.
        """
        checked_pairs = set()
        for prop1_node_id, prop1 in propositions_id_pairs.items():
            for prop2_node_id, prop2 in propositions_id_pairs.items():
                if prop1_node_id != prop2_node_id:
                    pair1 = (prop1_node_id, prop2_node_id)
                    pair2 = (prop2_node_id, prop1_node_id)
                    if pair1 not in checked_pairs and pair2 not in checked_pairs:
                        checked_pairs.add(pair1)
                        checked_pairs.add(pair2)
                        prediction = self.DamArgumentRelationAnalyzer.get_argument_relation((prop1, prop2)) 
                        if prediction in ['RA','MA','CA']:
                            xaif_obj.add_component("argument_relation", prediction, prop1_node_id, prop2_node_id)
                       
    

