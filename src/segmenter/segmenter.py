"""This file provides a simple segmenter that splits texts based on regex. 
The default segmenter takes xAIF, segments the texts in each L-node, 
introduces new L-node entries for each of the new segments, and deletes the old L-node entries.
"""

import re
from flask import json
import logging
from xaif_eval import xaif
logging.basicConfig(datefmt='%H:%M:%S',
                    level=logging.DEBUG)

class Segmenter():
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
		
	def _get_segments(self, input_text):
		"Simple segementer spliting texts based on regex."
		return re.split("[.!?]",input_text)

	def get_segments(self, input_data):
		"""The default segmenter takes xAIF, segments the texts in each L-nodes,
		introduce new L-node entries for each of the new segements and delete the old L-node entries
		"""	
		if self.is_json(input_data):
			xaif_obj = xaif.AIF(input_data)				
			if xaif_obj.is_valid_json_aif():
				json_dict = xaif_obj.aif
				nodes = json_dict['nodes']		
				for nodes_entry in nodes:
					node_id = nodes_entry['nodeID']
					node_text = nodes_entry['text']
					type = nodes_entry['type']
					if type == "L":
						segments = self._get_segments(node_text)
						segments = [seg.strip() for seg in segments if len(seg.strip()) > 1]
						if len(segments) > 1:
							for segment in segments:								
								if segment != "":	
									xaif_obj.add_component("segment", node_id, segment)										


				return xaif_obj.xaif
			else:
				return("Invalid json-aif")
		else:
			return("Invalid input")
	