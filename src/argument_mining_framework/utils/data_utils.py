from itertools import combinations
import torch
from typing import Dict, List
import re
from typing import Union, List, Tuple, Dict, Any
import json


class Data:
    def __init__(self,):
        pass
    
    def load_data(self, data: Union[str, Tuple[str, str], List[Tuple[str, str]], Dict[str, Any]], task_name=None) -> Dict[str, Any]:
        """Process data based on its type."""
        # Initialize the dictionary with default empty values
        if task_name in ["hypothesis", "scheme"]:
            if isinstance(data, str) or isinstance(data, list):
                return data, None
            elif isinstance(data, list) and all(isinstance(item, dict) for item in data):
                return [node.get("text") for node in data if node.get("type") == "I"], None



        result = {
            "argument": [],
            "prop_1": [],
            "prop_2": []
        }
        
        if isinstance(data, str):
            # Split the string into sentences using sentence delimiters.
            sentences = re.split(r'(?<=[.!?])\s+', data.strip())
            if len(sentences) >= 2:
                result["argument"] = " [SEP] ".join(sentences[:2])
                result["prop_1"] = [sentences[0]]
                result["prop_2"] = [sentences[1]]

        elif isinstance(data, tuple):
            result["argument"] = " [SEP] ".join(data)
            result["prop_1"] = [data[0]]
            result["prop_2"] = [data[1]]

        elif isinstance(data, list) and all(isinstance(item, tuple) for item in data):
            result["argument"] = [" [SEP] ".join(item) for item in data]
            result["prop_1"] = [item[0] for item in data]
            result["prop_2"] = [item[1] for item in data]

        elif isinstance(data, list) and all(isinstance(item, dict) for item in data):
            # Create a mapping of nodeID to text for all nodes of type "I"
            node_id_text_map = {node.get("nodeID"): node.get("text") for node in data if node.get("type") == "I"}

            # Join the extracted texts to form the argument string
            argument = " [SEP] ".join(node_id_text_map.values())

            # Generate combinations of node texts
            paired_texts = list(combinations(node_id_text_map.keys(), 2))

            for text_1, text_2 in paired_texts:
                result["prop_1"].append(node_id_text_map[text_1])
                result["prop_2"].append(node_id_text_map[text_2])
                result["argument"].append(argument)

        else:
            raise ValueError("Unsupported data type.")

        return result, paired_texts
    
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




    
class AIF:
    def __init__(self, ):
        pass
    def is_valid_json_aif(sel,aif_nodes):
        if 'nodes' in aif_nodes and 'locutions' in aif_nodes and 'edges' in aif_nodes:
            return True
        return False
    def is_json_aif_dialog(self, aif_nodes: list) -> bool:
        ''' check if json_aif is dialog
        '''

        for nodes_entry in aif_nodes:					
            if nodes_entry['type'] == "L":
                return True
        return False
    

        """
        This function takes a list of nodes and returns the maximum node ID.

        Arguments:
        - nodes (List[Dict]): a list of nodes, where each node is a dictionary containing a node ID

        Returns:
        - (int): the maximum node ID in the list of nodes
        """
        # Initialize a variable to store the maximum node ID found so far
        max_id  = 0
        lef_n_id, right_n_id = 0, ""

        if isinstance(nodes[0][n_type],str):
            if "_" in nodes[0][n_type]:
                
                #logging.debug('with hyphen')       
                # Loop through each node in the list of nodes
                for node in nodes:
                    # Check if the current node ID is greater than the current maximum
                    #logging.debug(node)
                    temp_id = node[n_type]
                    if "_" in temp_id:
                        nodeid_parsed = temp_id.split("_")
                        lef_n_id, right_n_id = int(nodeid_parsed[0]), nodeid_parsed[1]
                        if lef_n_id > max_id:
                            max_id = lef_n_id
                #logging.debug(str(int(max_id)+1)+"_"+str(right_n_id))
                return str(int(max_id)+1)+"_"+str(right_n_id)
            else:
                for node in nodes:
                    # Check if the current node ID is greater than the current maximum
                    temp_id = int(node[n_type])     
                    if temp_id > max_id:
                        # If it is, update the maximum to the current node ID
                        max_id = temp_id   
                # Return the maximum node ID found
                return str(max_id+1)

        elif isinstance(nodes[0][n_type],int):	
            for node in nodes:
                # Check if the current node ID is greater than the current maximum
                temp_id = node[n_type]     
                if temp_id > max_id:
                    # If it is, update the maximum to the current node ID
                    max_id = temp_id   
            # Return the maximum node ID found
            return max_id+1
    def get_next_max_id(self, nodes, n_type):
        """
       Takes a list of nodes (edges) and returns the maximum node/edge ID.
        Arguments:
        - nodes/edges (List[Dict]): a list of nodes/edges, where each node is a dictionary containing a node/edge ID
        Returns:
        - (int): the maximum node/edge ID in the list of nodes
        """

        max_id, lef_n_id, right_n_id = 0, 0, ""
        if isinstance(nodes[0][n_type],str): # check if the node id is a text or integer
            if "_" in nodes[0][n_type]:
                for node in nodes:
                    temp_id = node[n_type]
                    if "_" in temp_id:
                        nodeid_parsed = temp_id.split("_") # text node id can involve the character "_"
                        lef_n_id, right_n_id = int(nodeid_parsed[0]), nodeid_parsed[1]
                        if lef_n_id > max_id:
                            max_id = lef_n_id
                return str(int(max_id)+1)+"_"+str(right_n_id)
            else:
                for node in nodes:
                    temp_id = int(node[n_type])     
                    if temp_id > max_id:
                        max_id = temp_id   
                return str(max_id+1)

        elif isinstance(nodes[0][n_type],int):	
            for node in nodes:
                temp_id = node[n_type]     
                if temp_id > max_id:
                    max_id = temp_id   
            return max_id+1
        


    def get_speaker(self, 
        node_id: int, 
        locutions: List[Dict[str, int]], 
        participants: List[Dict[str, str]]
        ) -> str:
        """
        Takes a node ID, a list of locutions, and a list of participants, and returns the name of the participant who spoke the locution with the given node ID, or "None" 
        if the node ID is not found.

        Arguments:
        - node_id (int): the node ID to search for
        - locutions (List[Dict]): a list of locutions, where each locution is a dictionary containing a node ID and a person ID
        - participants (List[Dict]): a list of participants, where each participant is a dictionary containing a participant ID, a first name, and a last name

        Returns:
        - (str): the name of the participant who spoke the locution with the given node ID, or "None" if the node ID is not found
        """

        nodeID_speaker = {}
        # Loop through each locution and extract the person ID and node ID
        for locution in locutions:
            personID = locution['personID']
            nodeID = locution['nodeID']
            
            # Loop through each participant and check if their participant ID matches the person ID from the locution
            for participant in participants:
                if participant["participantID"] == personID:
                    # If there is a match, add the participant's name to the nodeID_speaker dictionary with the node ID as the key
                    firstname = participant["firstname"]
                    surname = participant["surname"]
                    nodeID_speaker[nodeID] = (firstname+" "+surname,personID)
                    
        # Check if the given node ID is in the nodeID_speaker dictionary and return the corresponding speaker name, or "None" if the node ID is not found
        if node_id in nodeID_speaker:
            return nodeID_speaker[node_id]
        else:
            return ("None None","None")

    def create_turn_entry(
        self,
        nodes, 
        node_id,
        person_id, 
        text_with_span,
        propositions,
        locutions,
        participants,
        dialogue 
        ):
        if dialogue:
            for first_and_last_names, proposition in propositions:
                first_last_names = first_and_last_names.split()
                first_names, last_names = "None", "None"
                if len(first_last_names) > 1:
                    first_names,last_names = first_last_names[0],first_last_names[1]
                else:
                    first_names, last_names = first_last_names[0],"None"
                text = proposition.replace("\n","")
                nodes.append({'text': text, 'type':'L','nodeID': node_id})
                locutions.append({'personID': person_id, 'nodeID': node_id})
                # Check if the entry already exists based on first name and surname
                if not any(participant['firstname'] == first_names and participant['surname'] == last_names for participant in participants):
                    participants.append({
                        "participantID": person_id,
                        "firstname": first_names,
                        "surname": last_names
                    })
                text_with_span = text_with_span+" "+first_names+" "+last_names+" "+"<span class=\"highlighted\" id=\""+str(node_id)+"\">"+text+"</span>.<br><br>"
                node_id = node_id + 1 
                person_id = person_id + 1


        else:
            text = propositions.replace("\n","")
            speaker = "Default Speaker"
            nodes.append({'text': text, 'type':'L','nodeID': node_id})	
            locutions.append({'personID': 1, 'nodeID': node_id})
            if not any(participant['firstname'] == "Default" and participant['surname'] == "Speaker" for participant in participants):
                participants.append(
                        {
                        "participantID": 1,                                
                        "firstname": "Default",                                
                        "surname": "Speaker"
                        }
                    )	
            text_with_span=text_with_span+" "+speaker+" "+"<span class=\"highlighted\" id=\""+str(node_id)+"\">"+text+"</span>.<br><br>"
            node_id = node_id + 1
        return (
            nodes, 
            locutions,
            participants, 
            text_with_span, 
            node_id,
            person_id
            )
    
    def get_i_node_ya_nodes_for_l_node(self, edges, n_id):
        """traverse through edges and returns YA node_ID and I node_ID, given L node_ID"""
        for entry in edges:
            if n_id == entry['fromID']:
                ya_node_id = entry['toID']
                for entry2 in edges:
                    if ya_node_id == entry2['fromID']:
                        inode_id = entry2['toID']
                        return(inode_id, ya_node_id)
        return None, None
    

    def remove_entries(self, l_node_id, nodes, edges, locutions):
        """
        Removes entries associated with a specific node ID from a JSON dictionary.

        Arguments:
        - node_id (int): the node ID to remove from the JSON dictionary
        - json_dict (Dict): the JSON dictionary to edit

        Returns:
        - (Dict): the edited JSON dictionary with entries associated with the specified node ID removed
        """
        # Remove nodes with the specified node ID
        in_id, yn_id = self.get_i_node_ya_nodes_for_l_node(edges, l_node_id)
        edited_nodes = [node for node in nodes if node.get('nodeID') != l_node_id]
        edited_nodes = [node for node in edited_nodes if node.get('nodeID') != in_id]

        # Remove locutions with the specified node ID
        edited_locutions = [node for node in locutions if node.get('nodeID') != l_node_id]

        # Remove edges with the specified node ID
        edited_edges = [node for node in edges if not (node.get('fromID') == l_node_id or node.get('toID') == l_node_id)]
        edited_edges = [node for node in edited_edges if not (node.get('fromID') == in_id or node.get('toID') == in_id)]
        edited_nodes = [node for node in edited_nodes if node.get('nodeID') != yn_id]
        # Return the edited JSON dictionary
        return edited_nodes, edited_edges, edited_locutions
    

    def get_xAIF_arrays(self, aif_section, xaif_elements) -> tuple:
        """
        Extracts values associated with specified keys from the given AIF section dictionary.

        Args:
            aif_section (dict): A dictionary containing AIF section information.
            xaif_elements (List): A list of keys for which values need to be extracted from the AIF section.

        Returns:
            tuple: A tuple containing values associated with the specified keys from the AIF section.
        """
        # Extract values associated with specified keys from the AIF section dictionary
        # If a key is not present in the dictionary, returns an empty list as the default value
        return tuple(aif_section.get(element) for element in xaif_elements)


	




def get_next_max_id(nodes, n_type):
    """
    This function takes a list of nodes and returns the maximum node ID.

    Arguments:
    - nodes (List[Dict]): a list of nodes, where each node is a dictionary containing a node ID

    Returns:
    - (int): the maximum node ID in the list of nodes
    """
    # Initialize a variable to store the maximum node ID found so far
    max_id  = 0
    lef_n_id, right_n_id = 0, ""

    if isinstance(nodes[0][n_type],str):
        if "_" in nodes[0][n_type]:
            
            #logging.debug('with hyphen')       
            # Loop through each node in the list of nodes
            for node in nodes:
                # Check if the current node ID is greater than the current maximum
                #logging.debug(node)
                temp_id = node[n_type]
                if "_" in temp_id:
                    nodeid_parsed = temp_id.split("_")
                    lef_n_id, right_n_id = int(nodeid_parsed[0]), nodeid_parsed[1]
                    if lef_n_id > max_id:
                        max_id = lef_n_id
            #logging.debug(str(int(max_id)+1)+"_"+str(right_n_id))
            return str(int(max_id)+1)+"_"+str(right_n_id)
        else:
            for node in nodes:
                # Check if the current node ID is greater than the current maximum
                temp_id = int(node[n_type])     
                if temp_id > max_id:
                    # If it is, update the maximum to the current node ID
                    max_id = temp_id   
            # Return the maximum node ID found
            return str(max_id+1)

    elif isinstance(nodes[0][n_type],int):	
        for node in nodes:
            # Check if the current node ID is greater than the current maximum
            temp_id = node[n_type]     
            if temp_id > max_id:
                # If it is, update the maximum to the current node ID
                max_id = temp_id   
        # Return the maximum node ID found
        return max_id+1

