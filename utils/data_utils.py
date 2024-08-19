from itertools import combinations
import torch

class Data:
    """
    A class for handling data related to argument and proposition processing.

    Methods:
        load_data(nodes): Loads and prepares data from given nodes.
        prepare_inputs(data, context=False): Prepares input strings for the model.
    """
    
    def load_data(self, nodes):
        """
        Loads and prepares data from given nodes.

        Args:
            nodes (list): List of node dictionaries, each containing 'nodeID', 'text', and 'type'.

        Returns:
            Tuple: (data, paired_texts)
                - data (dict): Contains arguments and propositions for the pairs of nodes.
                - paired_texts (list): List of tuples containing pairs of node IDs.
        """
        # Create a mapping of nodeID to text for all nodes of type "I"
        node_id_text_map = {node.get("nodeID"): node.get("text") for node in nodes if node.get("type") == "I"}
        
        # Join the extracted texts to form the argument string
        argument = " '[SEP]' ".join(node_id_text_map.values())
        
        # Generate combinations of node texts
        paired_texts = list(combinations(node_id_text_map.keys(), 2))
        
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
        """
        Prepares input strings for the model.

        Args:
            data (dict): Contains arguments and propositions for the pairs of nodes.
            context (bool): If True, includes context information in the input string.

        Returns:
            list: List of input strings prepared for the model.
        """
        inputs_data = []
        arguments = data['argument']
        list_proposition1 = data['prop_1']
        list_proposition2 = data['prop_2']
        
        for proposition1, proposition2, argument in zip(list_proposition1, list_proposition2, arguments):
            if context:
                input_data = f"{argument} '[SEP]' {proposition1} '[SEP]' {proposition2}"
            else:
                input_data = f"{proposition1} '[SEP]' {proposition2}"
            inputs_data.append(input_data)
        
        return inputs_data

def get_distance_based_positional_embedding(distance, p_dim):
    """
    Computes positional embeddings based on distance for a given dimension.

    Args:
        distance (int): The distance used to calculate the positional embedding.
        p_dim (int): The dimensionality of the positional embeddings.

    Returns:
        torch.Tensor: The computed positional embeddings.
    """
    # Calculate angles for sine and cosine
    angles = torch.arange(0, p_dim, 2.0) * -(1.0 / torch.pow(10000, (torch.arange(0.0, p_dim, 2.0) / p_dim)))
    
    # Calculate positional embeddings using sine and cosine functions
    positional_embeddings = torch.zeros(1, p_dim)
    positional_embeddings[:, 0::2] = torch.sin(distance * angles)
    positional_embeddings[:, 1::2] = torch.cos(distance * angles)

    return positional_embeddings
