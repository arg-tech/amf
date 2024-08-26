import re
from flask import json
import logging
from xaif_eval import xaif

from amf.utils.data_utils import AIF
from amf.utils.output import TurninatorOutput

logging.basicConfig(datefmt='%H:%M:%S', level=logging.DEBUG)


class Turninator():
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


    
    def dialog_turns(self, text: str):
        '''Extract dialog turns from input text using regex.'''
        # Remove any HTML tags
        text = re.sub('<.*?>', '', text, flags=re.DOTALL)
        # Regular expression to capture speaker and their corresponding text
        return re.findall(r'([A-Za-z0-9 ]+)\s*:\s*((?:.|\n)*?)(?=\n[A-Za-z0-9 ]+\s*:\s*|\Z)', text)

    def monolog_text(self, text: str) -> str:
        '''Extract the entire text if monolog.'''
        return re.sub('<.*?>', '', text, flags=re.DOTALL)


    def get_turns(self, input_data, dialogue=False):
        AIF_obj = AIF()
        extended_json_aif = {}
        if self.is_json(input_data):
            xaif_obj = xaif.AIF(input_data)                 
            if xaif_obj.is_valid_json_aif():				
                nodes, edges, locutions = [], [], []
                extended_json_aif = xaif_obj.xaif
                if 'AIF' in extended_json_aif and 'text' in extended_json_aif:
                    json_dict = extended_json_aif['AIF'] 
                    dialog = extended_json_aif.get('dialog', False)
                    OVA = extended_json_aif.get('OVA', [])
                    # Handle the case where 'json_dict' is a string
                    if isinstance(json_dict, str):
                        if json_dict.startswith('"'):
                            json_dict = json_dict.replace("\"", "")
                            json_dict = dict(json_dict)
                            logging.info(f'processing monolog text in json extenssion')
                    if not isinstance(json_dict, dict):
                        json_dict = json.loads(json_dict)
                    # Extract values associated with specific keys from the AIF section
                    schemefulfillments, descriptorfulfillments = AIF_obj.get_xAIF_arrays(aif_section=json_dict,
                                                                                     xaif_elements=['schemefulfillments', 'descriptorfulfillments'])
                    logging.info(f"xAIF valid:  {is_json_file}")  
                    participants = json_dict.get("participants", [])
                    if isinstance(extended_json_aif['text'], dict):
                        text = extended_json_aif['text']['txt']
                        logging.info(f'text with dict')
                    else:
                        text = extended_json_aif['text']  # gets the text
                        text = text + "\n"
                        logging.info(f'text without dict')
                        #logging.info(f'text :{text}')
                    if isinstance(text, str):
                        json_object = json.dumps(text)
                        json_object = json.loads(json_object) 
                        logging.info(f'text dumped')                   
                    is_dialog = extended_json_aif.get('dialog')
                    text_with_span = ""
                    node_id, person_id = 0, 0
                    # Extract dialog turns if it's a dialog, otherwise extract monolog text
                    logging.info(f'text : {text}')
                    logging.info(f'is dialog : {is_dialog}')
                    speakers_and_turns = self.dialog_turns(text) if is_dialog and len(self.dialog_turns(text)) else self.monolog_text(text)
                    if is_dialog and len(self.dialog_turns(text)):
                        logging.info(f'processing dialog text from text format')
                        speakers_and_turns = self.dialog_turns(text)
                        nodes, locutions, participants, text_with_span, node_id, person_id = AIF_obj.create_turn_entry(
                            nodes, node_id, person_id, text_with_span, speakers_and_turns, locutions, participants, is_dialog)
                    else:
                        if not is_dialog:
                            logging.info(f'processing monolog text since not dialog')
                            speakers_and_turns = self.monolog_text(text)
                            nodes, locutions, participants, text_with_span, node_id, person_id = AIF_obj.create_turn_entry(
                                nodes, node_id, person_id, text_with_span, speakers_and_turns, locutions, participants, is_dialog)
                    return TurninatorOutput.format_output(nodes, edges, locutions, 
                                                          schemefulfillments, descriptorfulfillments, participants, 
                                                          OVA, text_with_span, dialog, json_dict, extended_json_aif)
                else:
                    if 'text' in extended_json_aif:
                        node_id, person_id = 0, 0
                        if isinstance(extended_json_aif['text'], dict):
                            text = extended_json_aif['text']['txt']
                        else:
                            text = extended_json_aif['text'] + "\n"
                        
                        aif, json_aif, OVA = {}, {}, {}      
                        text_with_span = ""
                        nodes, edges, schemefulfillments, descriptorfulfillments, participants, locutions = [], [], [], [], [], []
                        speakers_and_turns = self.monolog_text(text)                   
                        nodes, locutions, participants, text_with_span, node_id, person_id = AIF_obj.create_turn_entry(
                            nodes, node_id, person_id, text_with_span, speakers_and_turns, locutions, participants, False)
                        return TurninatorOutput.format_output(nodes, edges, locutions, schemefulfillments, descriptorfulfillments, participants, OVA, text_with_span, aif, extended_json_aif)
            else:
                return "Invalid json"
        else:
            # Non-json data is treated as monolog
            node_id, person_id = 0, 0        
            aif, json_aif, OVA = {}, {}, {}       
            text_with_span = ""
            nodes, edges, schemefulfillments, descriptorfulfillments, participants, locutions = [], [], [], [], [], []
            if dialogue:
                speakers_and_turns = self.dialog_turns(input_data)   
                nodes, locutions, participants, text_with_span, node_id, person_id = AIF_obj.create_turn_entry(
                nodes, node_id, person_id, text_with_span, speakers_and_turns, locutions, participants, True)
            else:
                speakers_and_turns = self.monolog_text(input_data) 
                print(speakers_and_turns)                   
                nodes, locutions, participants, text_with_span, node_id, person_id = AIF_obj.create_turn_entry(
                    nodes, node_id, person_id, text_with_span, speakers_and_turns, locutions, participants, False)
            return TurninatorOutput.format_output(nodes, edges, locutions, schemefulfillments, descriptorfulfillments, participants, OVA, text_with_span,aif, json_aif)



