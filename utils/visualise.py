import requests
import json
import io
from IPython.display import display, SVG
import webbrowser
import tempfile
import os

class JsonToSvgConverter:
    def __init__(self,):
        self.url = 'http://svg.amfws.arg.tech'

    def convert(self, json_data):
        json_data = json.dumps(json_data)
        try:
            headers = {'Content-Type': 'application/json'}
            response = requests.post(self.url, headers=headers, data=json_data)
            response.raise_for_status()  # Raise an HTTPError if the response was an HTTP error
        except requests.exceptions.RequestException as e:
            print(f'An error occurred during the request: {e}')
            return None

        if response:
            try:
                # Check if the response is SVG content
                if 'image/svg+xml' in response.headers.get('Content-Type', ''):
                    print('SVG response received:')
                    return response.text
                else:
                    print(f'The response is not in SVG format. Content-Type: {response.headers.get("Content-Type")}')
                    print(f'First 100 characters of response content: {response.text[:100]}')
                    return response.text
            except Exception as e:
                print(f'An error occurred while processing the response: {e}')
                return None
        else:
            print('No response received.')
            return None

    def visualize_svg(self, svg_content):
        # Option 1: Display in Jupyter Notebook or IPython environment
        if 'IPython' in globals():
            display(SVG(svg_content))
        else:
            # Option 2: Create a temporary HTML file and open it in the browser
            with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as tmp:
                tmp.write(f'<html><body>{svg_content}</body></html>'.encode('utf-8'))
                webbrowser.open(f'file://{tmp.name}')
    def visualise(self, argument_map_output):        
        converter = JsonToSvgConverter()
        #json_aif = argument_map_output['AIF']
        svg_output = converter.convert(argument_map_output)
        if svg_output:
            converter.visualize_svg(svg_output)

# Example usage
if __name__ == "__main__":
    url = 'http://svg.amfws.arg.tech'
    #url = 'http://ws.arg.tech/t/json-svg'

    json_data = {"AIF": {"nodes": [{"nodeID": "1", "text": "THANK YOU", "type": "I", "timestamp": "2016-10-31 17:17:34"},
 {"nodeID": "2", "text": "COOPER : THANK YOU", "type": "L", "timestamp": "2016-11-10 18:34:23"},
  {"nodeID": "3", "text": "You are well come", "type": "I", "timestamp": "2016-10-31 17:17:34"},
   {"nodeID": "4", "text": "Bob : You are well come", "type": "L", "timestamp": "2016-11-10 18:34:23"}, 
   {"nodeID": "5", "text": "does or doesnt Jeane Freeman think the SNP is divided with what is going on", "type": "I", "timestamp": ""}, 
   {"nodeID": "6", "text": "the SNP is a big party", "type": "I", "timestamp": ""}, {"nodeID": "20", "text": "Default Inference", "type": "RA", "timestamp": ""}, 
   {"nodeID": "7", "text": "would or wouldnt Jeane Freeman describe the SNP as united", "type": "I", "timestamp": ""}, 
   {"nodeID": "8", "text": "the SNP has disagreements", "type": "I", "timestamp": ""}, 
   {"nodeID": "9", "text": "the SNP has disagreements", "type": "I", "timestamp": ""},
    {"nodeID": "10", "text": "Michael Forsyth belongs to a party that has disagreements", "type": "I", "timestamp": ""}, 
    {"nodeID": "11", "text": "one disagreement of Michael Forsyths party is currently about their Scottish leader", "type": "I", "timestamp": ""}, 
    {"nodeID": "12", "text": "Iain Murray has had disagreements with his party", "type": "I", "timestamp": ""},
     {"nodeID": "13", "text": "its not uncommon for there to be disagreements between party members", "type": "I", "timestamp": ""},
      {"nodeID": "14", "text": "disagreements between party members are entirely to be expected", "type": "I", "timestamp": ""}, 
      {"nodeID": "15", "text": "what isnt acceptable is any disagreements are conducted that is disrespectful of other points of view", "type": "I", "timestamp": ""},
       {"nodeID": "16", "text": "Jeanne Freeman wants to be in a political party and a country where different viewpoints and different arguments, Donald Dyer famously said, are conducted with respect and without abuse", "type": "I", "timestamp": ""}, 
       {"nodeID": "17", "text": "who does or doesnt Jeanne Freeman think is being disrespectful then", "type": "I", "timestamp": ""},
        {"nodeID": "18", "text": "people feel, when they have been voicing opinions on different matters, that they have been not listened to", "type": "I", "timestamp": ""}, 
        {"nodeID": "19", "text": "people feel that they have been treated disrespectfully. on all sides of the different arguments and disputes going on", "type": "L", "timestamp": ""}, 
        {"text": "Default Conflict", "type": "CA", "nodeID": "21"}, {"text": "Default Conflict", "type": "CA", "nodeID": "22"}, 
        {"text": "Default Inference", "type": "RA", "nodeID": "23"}, {"text": "Default Inference", "type": "RA", "nodeID": "24"}, {"text": "Default Inference", "type": "RA", "nodeID": "25"}, {"text": "Default Inference", "type": "RA", "nodeID": "26"}, {"text": "Default Inference", "type": "RA", "nodeID": "27"}, {"text": "Default Inference", "type": "RA", "nodeID": "28"}, {"text": "Default Inference", "type": "RA", "nodeID": "29"}, {"text": "Default Inference", "type": "RA", "nodeID": "30"}, {"text": "Default Inference", "type": "RA", "nodeID": "31"}, {"text": "Default Inference", "type": "RA", "nodeID": "32"}], "edges": [{"edgeID": "1", "fromID": "1", "toID": "20", "formEdgeID": "None"}, {"edgeID": "2", "fromID": "20", "toID": "3", "formEdgeID": "None"}, {"fromID": "1", "toID": "21", "edgeID": "3"}, {"fromID": "21", "toID": "3", "edgeID": "4"}, {"fromID": "3", "toID": "22", "edgeID": "5"}, {"fromID": "22", "toID": "7", "edgeID": "6"}, {"fromID": "7", "toID": "23", "edgeID": "7"}, {"fromID": "23", "toID": "8", "edgeID": "8"}, {"fromID": "8", "toID": "24", "edgeID": "9"}, {"fromID": "24", "toID": "9", "edgeID": "10"}, {"fromID": "9", "toID": "25", "edgeID": "11"}, {"fromID": "25", "toID": "10", "edgeID": "12"}, {"fromID": "10", "toID": "26", "edgeID": "13"}, {"fromID": "26", "toID": "15", "edgeID": "14"}, {"fromID": "6", "toID": "27", "edgeID": "15"}, {"fromID": "27", "toID": "14", "edgeID": "16"}, {"fromID": "5", "toID": "28", "edgeID": "17"}, {"fromID": "28", "toID": "10", "edgeID": "18"}, {"fromID": "5", "toID": "29", "edgeID": "19"}, {"fromID": "29", "toID": "12", "edgeID": "20"}, {"fromID": "13", "toID": "30", "edgeID": "21"}, {"fromID": "30", "toID": "16", "edgeID": "22"}, {"fromID": "11", "toID": "31", "edgeID": "23"}, {"fromID": "31", "toID": "16", "edgeID": "24"}, {"fromID": "11", "toID": "32", "edgeID": "25"}, {"fromID": "32", "toID": "18", "edgeID": "26"}], "locutions": [], "participants": []}, "text": "people feel that they have been treated disrespectfully. on all sides of the different arguments and disputes going on"}
    '''
    json_data = {
            'nodes': [
                {'text': 'Vaccines mark a major advance in human achievement...', 'type': 'L', 'nodeID': 2},
                {'text': 'But this isn’t the time for vaccine nationalism', 'type': 'L', 'nodeID': 3},
                {'text': 'I agree we should congratulate all the scientists...', 'type': 'L', 'nodeID': 4},
                # More nodes...
            ],
            'edges': [
                {'toID': 15, 'fromID': 2, 'edgeID': 0},
                {'toID': 14, 'fromID': 15, 'edgeID': 1},
                # More edges...
            ],
            # Other elements like locutions, schemefulfillments, etc...
        }
    '''
    converter = JsonToSvgConverter()
    svg_output = converter.convert(json_data)
    if svg_output:
        converter.visualize_svg(svg_output)
