
from itertools import combinations
import torch


class Data:
    def load_data(self, nodes):
        # Create a mapping of nodeID to text for all nodes of type "I"
        node_id_text_map = {node.get("nodeID"): node.get("text") for node in nodes if node.get("type") == "I"}       
        # Join the extracted texts to form the argument string
        argument = " '[SEP]' ".join(node_id_text_map.values())
        paired_texts = list(combinations(node_id_text_map.keys(), 2))  # Generate combinations of node texts       
        proposition_1, proposition_2, arguments = [], [], []        
        for text_1, text_2 in paired_texts:
            proposition_1.append(node_id_text_map[text_1])
            proposition_2.append(node_id_text_map[text_2])
            arguments.append(argument)
        
        data = {
            "argument": arguments,
            "prop_1": proposition_1,
            "prop_2": proposition_2
        }
        
        return data, paired_texts
    
    def prepare_inputs(self, data, context=False):
       
        inputs_data = []
        arguments = data['argument']
        list_proposition1 = data['prop_1']
        list_proposition2 = data['prop_2']
        for proposition1, proposition2, argument in zip(list_proposition1, list_proposition2, arguments):
            if context:
                input_data= f"{argument} {proposition1} ' [SEP] ' {proposition2}"
            else:
                input_data= f"{proposition1} ' [SEP] ' {proposition2}"
            inputs_data.append(input_data)
        return inputs_data


def get_distance_based_positional_embedding(distance, p_dim):
    # Calculate angles for sine and cosine
    angles = torch.arange(0, p_dim, 2.0) * -(1.0 / torch.pow(10000, (torch.arange(0.0, p_dim, 2.0) / p_dim)))

    # Calculate positional embeddings using sine and cosine functions
    positional_embeddings = torch.zeros(1, p_dim)
    positional_embeddings[:, 0::2] = torch.sin(distance * angles)
    positional_embeddings[:, 1::2] = torch.cos(distance * angles)

    return positional_embeddings