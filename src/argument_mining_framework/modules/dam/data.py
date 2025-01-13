import json
from typing import Dict, List


def get_file(file_obj):
    f_name = file_obj.filename    
    file_obj.save(f_name)
    file = open(f_name,'r')
    return f_name

class Data:
    def __init__(self, file_obj):
        self.file_obj = file_obj
        self.f_name = file_obj.filename
        self.file_obj.save(self.f_name)
        file = open(self.f_name,'r')

    def is_valid_json(self):
        ''' check if the file is valid json
		'''

        try:
            json.loads(open(self.f_name).read())
        except ValueError as e:			
            return False

        return True
    def is_valid_json_aif(sel,aif_nodes):
        if 'nodes' in aif_nodes and 'locutions' in aif_nodes and 'edges' in aif_nodes:
            return True
        return False
        

    def get_aif(self, format='xAIF'):
        if self.is_valid_json():
            with open(self.f_name) as file:
                data = file.read()
                x_aif = json.loads(data)
                if format == "xAIF":
                    return x_aif
                else:
                    aif = x_aif.get('AIF')
                    return json.dumps(aif)
        else:
            return "Invalid json"
        
    def get_file_path(self,):
            return self.f_name
    
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
        


    def get_speaker(self, node_id: int, locutions: List[Dict[str, int]], participants: List[Dict[str, str]]) -> str:
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

    def create_entry(self,nodes, edges, prediction, index1, index2):
        if prediction == "RA":
            node_id = self.get_next_max_id(nodes, 'nodeID')
            edge_id = self.get_next_max_id(edges, 'edgeID')		
            nodes.append({'text': 'Default Inference', 'type':'RA','nodeID': node_id})					
            edges.append({'fromID': index1, 'toID': node_id,'edgeID':edge_id})	
            edge_id = self.get_next_max_id(edges, 'edgeID')				
            edges.append({'fromID': node_id, 'toID': index2,'edgeID':edge_id})

        if prediction == "CA":				
            node_id = self.get_next_max_id(nodes, 'nodeID')
            edge_id = self.get_next_max_id(edges, 'edgeID')
            nodes.append({'text': 'Default Conflict', 'type':'CA','nodeID': node_id})				
            edges.append({'fromID': index1, 'toID': node_id,'edgeID':edge_id})
            edge_id = self.get_next_max_id(edges, 'edgeID')
            edges.append({'fromID': node_id, 'toID': index2,'edgeID':edge_id})
            
        return (nodes, edges)
    
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
    

    def get_xAIF_arrays(self, aif_section: dict, xaif_elements: List) -> tuple:
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


