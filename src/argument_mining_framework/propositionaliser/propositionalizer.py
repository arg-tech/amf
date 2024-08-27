

import logging
from argument_mining_framework.utils.data_utils import get_next_max_id
import json
import logging
from xaif_eval import xaif

logging.basicConfig(datefmt='%H:%M:%S',
                    level=logging.DEBUG)



class Propositionalizer():
	def __init__(self,):
		pass

	def is_json(self, input_data):
		if isinstance(input_data, dict):
			# If the input is already a dictionary, it's JSON-like data
			return True

		try:
			# Try to parse the string as JSON
			json.loads(input_data)
			return True
		except (ValueError, TypeError):
			# If parsing fails, it's not JSON
			return False


	def get_propositions(self,input_data):
		if self.is_json(input_data):
			xaif_obj = xaif.AIF(input_data)				
			if xaif_obj.is_valid_json_aif():
				json_dict = xaif_obj.aif
				nodes, edges  = json_dict['nodes'], json_dict['edges']				
				original_nodes = nodes.copy()			
				i_nodes_lis = []
				for nodes_entry in original_nodes:
					propositions = nodes_entry['text']
					node_id = nodes_entry['nodeID'] 
					if propositions not in i_nodes_lis:
						if nodes_entry['type'] == "L":						
							inode_id = get_next_max_id(nodes, "nodeID")
							nodes.append({'text': propositions, 'type':'I','nodeID': inode_id})
							i_nodes_lis.append(propositions)
							y_id = get_next_max_id(nodes, "nodeID")
							nodes.append({'text': 'Default Illocuting', 'type':'YA','nodeID': y_id})
							if edges:	
								edge_id = get_next_max_id(edges, "edgeID")
							else:
								edge_id = 0
							edges.append({'toID': y_id, 'fromID':node_id,'edgeID': edge_id})
							edge_id = get_next_max_id(edges, "edgeID")
							edges.append({'toID': inode_id, 'fromID':y_id,'edgeID': edge_id})

				return xaif_obj.xaif
			else:
				return("Incorrect json-aif format")
		else:
			return("Incorrect input format")




