from typing import Dict, List
import re
import numpy as np
from nltk import ngrams
from collections import defaultdict


    
def top_freq_list(xs, top):
    counts = defaultdict(int)
    for x in xs:
        counts[x] += 1
    return sorted(counts.items(), reverse=True, key=lambda tup: tup[1])[:top]

def get_file(file_obj):
    f_name = file_obj.filename    
    file_obj.save(f_name)
    file = open(f_name,'r')
    return f_name

  
def frequent_tuple(tuples):
    count_tuple={}
    for tup in tuples:
        #print('tup..............................................',tup)
        length=len(tup[0].split(" "))
        if length in count_tuple.keys():
            count_tuple[length]+=1
        else:
            count_tuple[length]=1
    sorted_dct=dict(sorted(count_tuple.items(), reverse=True,key=lambda item: item[1]))
    return next(iter( sorted_dct.items() ))[0] 
    
    

def identyfy_maxs_index(x,bar): 
    return x > bar

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

def get_speaker(
    nodeID_speaker,
    node_id: int, 
    locutions: List[Dict[str, int]], 
    participants: List[Dict[str, str]]
    ) -> str:
    """
    This function takes a node ID, a list of locutions, and a list of participants, and returns the name of the participant who spoke the locution with the given node ID, or "None" if the node ID is not found.

    Arguments:
    - node_id (int): the node ID to search for
    - locutions (List[Dict]): a list of locutions, where each locution is a dictionary containing a node ID and a person ID
    - participants (List[Dict]): a list of participants, where each participant is a dictionary containing a participant ID, a first name, and a last name

    Returns:
    - (str): the name of the participant who spoke the locution with the given node ID, or "None" if the node ID is not found
    """

    
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

def get_inode(edges, n_id):
    for entry in edges:
        if n_id == entry['fromID']:
            ya_node_id = entry['toID']
            for entry2 in edges:
                if ya_node_id == entry2['fromID']:
                    inode_id = entry2['toID']
                    return(inode_id, ya_node_id)
    return None, None