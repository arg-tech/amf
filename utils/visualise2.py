import requests
import json
import io
from IPython.display import display, SVG
import webbrowser
import tempfile

class JsonToSvgConverter:
    def __init__(self,):
        self.url = 'http://ws.arg.tech/t/json-svg'

    def convert(self, json_data):
        try:
            # Convert JSON data to a string and then to a file-like object
            #json_str = json.dumps(json_data)
            #json_file_like = io.BytesIO(json_str.encode('utf-8'))

            # Prepare the files dictionary to mimic file upload
            #files = {'file': ('input.json', json_file_like, 'application/json')}

            # Send the POST request
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, headers=headers, data=json_data)
            response.raise_for_status()  # Raise an HTTPError if the response was an HTTP error
        except requests.exceptions.RequestException as e:
            print(f'An error occurred during the request: {e}')
            return None

        if response:
            
            try:
                # Check if the response is SVG content
                if 'image/svg+xml' in response.headers.get('Content-Type', ''):
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
        json_aif = argument_map_output['AIF']
        svg_output = converter.convert(json_aif)
        if svg_output:
            converter.visualize_svg(svg_output)

# Example usage
if __name__ == "__main__":
    # URL for the SVG generation service
    url = 'http://ws.arg.tech/t/json-svg'

    # JSON data to be converted to SVG
    json_data =  {'nodes': 
                         [{'text': 'Vaccines mark a major advance in human achievement since the enlightenment into the 19th Century and Britain’s been at the forefront of those achievements over the years and decades', 'type': 'L', 'nodeID': 2}, {'text': 'But this isn’t the time for vaccine nationalism', 'type': 'L', 'nodeID': 3}, {'text': 'I agree we should congratulate all the scientists, those in Belgium, the States, British scientists working in international teams here in the UK, with AstraZeneca', 'type': 'L', 'nodeID': 4}, {'text': 'What about the logistical capabilities', 'type': 'L', 'nodeID': 5}, {'text': 'They are obviously forefront now, now we’ve got a vaccine that’s been approved', 'type': 'L', 'nodeID': 6}, {'text': 'It’s good -- I’m reassured that the British Army are going to be involved', 'type': 'L', 'nodeID': 7}, {'text': 'They’re absolute world experts at rolling out things, complex logistic capabilities', 'type': 'L', 'nodeID': 8}, {'text': 'This is probably going to be the biggest logistical exercise that our armed forces have undertaken since the Falklands War, which I’m old enough to remember, just about', 'type': 'L', 'nodeID': 9}, {'text': 'So, as a neutral I’d like to see a lot of cross-party cooperation, and I’m encouraged with Sarah’s tone, everybody wants to see us getting on with it now', 'type': 'L', 'nodeID': 10}, {'text': 'They don’t want to see competition on whose vaccine is best', 'type': 'L', 'nodeID': 11}, {'text': 'There will be some instances where the Pfizer vaccine works better, another where you can’t have cold refrigeration, across the developing world as well, a cheaper vaccine like the AstraZeneca works better', 'type': 'L', 'nodeID': 12}, {'text': 'Let’s keep our fingers crossed and hope we make a good job of this', 'type': 'L', 'nodeID': 13}, {'text': 'Vaccines mark a major advance in human achievement since the enlightenment into the 19th Century and Britain’s been at the forefront of those achievements over the years and decades', 'type': 'I', 'nodeID': 14}, {'text': 'Default Illocuting', 'type': 'YA', 'nodeID': 15}, {'text': 'But this isn’t the time for vaccine nationalism', 'type': 'I', 'nodeID': 16}, {'text': 'Default Illocuting', 'type': 'YA', 'nodeID': 17}, {'text': 'I agree we should congratulate all the scientists, those in Belgium, the States, British scientists working in international teams here in the UK, with AstraZeneca', 'type': 'I', 'nodeID': 18}, {'text': 'Default Illocuting', 'type': 'YA', 'nodeID': 19}, {'text': 'What about the logistical capabilities', 'type': 'I', 'nodeID': 20}, {'text': 'Default Illocuting', 'type': 'YA', 'nodeID': 21}, {'text': 'They are obviously forefront now, now we’ve got a vaccine that’s been approved', 'type': 'I', 'nodeID': 22}, {'text': 'Default Illocuting', 'type': 'YA', 'nodeID': 23}, {'text': 'It’s good -- I’m reassured that the British Army are going to be involved', 'type': 'I', 'nodeID': 24}, {'text': 'Default Illocuting', 'type': 'YA', 'nodeID': 25}, {'text': 'They’re absolute world experts at rolling out things, complex logistic capabilities', 'type': 'I', 'nodeID': 26}, {'text': 'Default Illocuting', 'type': 'YA', 'nodeID': 27}, {'text': 'This is probably going to be the biggest logistical exercise that our armed forces have undertaken since the Falklands War, which I’m old enough to remember, just about', 'type': 'I', 'nodeID': 28}, {'text': 'Default Illocuting', 'type': 'YA', 'nodeID': 29}, {'text': 'So, as a neutral I’d like to see a lot of cross-party cooperation, and I’m encouraged with Sarah’s tone, everybody wants to see us getting on with it now', 'type': 'I', 'nodeID': 30}, {'text': 'Default Illocuting', 'type': 'YA', 'nodeID': 31}, {'text': 'They don’t want to see competition on whose vaccine is best', 'type': 'I', 'nodeID': 32}, {'text': 'Default Illocuting', 'type': 'YA', 'nodeID': 33}, {'text': 'There will be some instances where the Pfizer vaccine works better, another where you can’t have cold refrigeration, across the developing world as well, a cheaper vaccine like the AstraZeneca works better', 'type': 'I', 'nodeID': 34}, {'text': 'Default Illocuting', 'type': 'YA', 'nodeID': 35}, {'text': 'Let’s keep our fingers crossed and hope we make a good job of this', 'type': 'I', 'nodeID': 36}, {'text': 'Default Illocuting', 'type': 'YA', 'nodeID': 37}, {'text': 'Default Inference', 'type': 'RA', 'nodeID': 38}, {'text': 'Default Inference', 'type': 'RA', 'nodeID': 39}, {'text': 'Default Inference', 'type': 'RA', 'nodeID': 40}, {'text': 'Default Inference', 'type': 'RA', 'nodeID': 41}, {'text': 'Default Inference', 'type': 'RA', 'nodeID': 42}, {'text': 'Default Inference', 'type': 'RA', 'nodeID': 43}, {'text': 'Default Conflict', 'type': 'CA', 'nodeID': 44}, {'text': 'Default Conflict', 'type': 'CA', 'nodeID': 45}], 
                         'edges': [{'toID': 15, 'fromID': 2, 'edgeID': 0}, {'toID': 14, 'fromID': 15, 'edgeID': 1}, {'toID': 17, 'fromID': 3, 'edgeID': 2}, {'toID': 16, 'fromID': 17, 'edgeID': 3}, {'toID': 19, 'fromID': 4, 'edgeID': 4}, {'toID': 18, 'fromID': 19, 'edgeID': 5}, {'toID': 21, 'fromID': 5, 'edgeID': 6}, {'toID': 20, 'fromID': 21, 'edgeID': 7}, {'toID': 23, 'fromID': 6, 'edgeID': 8}, {'toID': 22, 'fromID': 23, 'edgeID': 9}, {'toID': 25, 'fromID': 7, 'edgeID': 10}, {'toID': 24, 'fromID': 25, 'edgeID': 11}, {'toID': 27, 'fromID': 8, 'edgeID': 12}, {'toID': 26, 'fromID': 27, 'edgeID': 13}, {'toID': 29, 'fromID': 9, 'edgeID': 14}, {'toID': 28, 'fromID': 29, 'edgeID': 15}, {'toID': 31, 'fromID': 10, 'edgeID': 16}, {'toID': 30, 'fromID': 31, 'edgeID': 17}, {'toID': 33, 'fromID': 11, 'edgeID': 18}, {'toID': 32, 'fromID': 33, 'edgeID': 19}, {'toID': 35, 'fromID': 12, 'edgeID': 20}, {'toID': 34, 'fromID': 35, 'edgeID': 21}, {'toID': 37, 'fromID': 13, 'edgeID': 22}, {'toID': 36, 'fromID': 37, 'edgeID': 23}, {'fromID': 14, 'toID': 38, 'edgeID': 24}, {'fromID': 38, 'toID': 16, 'edgeID': 25}, {'fromID': 16, 'toID': 39, 'edgeID': 26}, {'fromID': 39, 'toID': 18, 'edgeID': 27}, {'fromID': 18, 'toID': 40, 'edgeID': 28}, {'fromID': 40, 'toID': 22, 'edgeID': 29}, {'fromID': 22, 'toID': 41, 'edgeID': 30}, {'fromID': 41, 'toID': 24, 'edgeID': 31}, {'fromID': 24, 'toID': 42, 'edgeID': 32}, {'fromID': 42, 'toID': 26, 'edgeID': 33}, {'fromID': 28, 'toID': 43, 'edgeID': 34}, {'fromID': 43, 'toID': 30, 'edgeID': 35}, {'fromID': 30, 'toID': 44, 'edgeID': 36}, {'fromID': 44, 'toID': 32, 'edgeID': 37}, {'fromID': 32, 'toID': 45, 'edgeID': 38}, {'fromID': 45, 'toID': 34, 'edgeID': 39}], 'locutions': [{'personID': 0, 'nodeID': 2}, {'personID': 'None', 'nodeID': 3}, {'personID': 'None', 'nodeID': 4}, {'personID': 1, 'nodeID': 5}, {'personID': 'None', 'nodeID': 6}, {'personID': 'None', 'nodeID': 7}, {'personID': 'None', 'nodeID': 8}, {'personID': 'None', 'nodeID': 9}, {'personID': 'None', 'nodeID': 10}, {'personID': 'None', 'nodeID': 11}, {'personID': 'None', 'nodeID': 12}, {'personID': 'None', 'nodeID': 13}], 'schemefulfillments': [], 'descriptorfulfillments': [], 'participants': [{'participantID': 0, 'firstname': 'Liam', 'surname': 'Halligan'}, {'participantID': 1, 'firstname': 'Fiona', 'surname': 'Bruce'}]
                         }

                        

    # Initialize the converter and perform the conversion
    converter = JsonToSvgConverter(url)
    svg_output = converter.convert(json_data)
    if svg_output:
        converter.visualize_svg(svg_output)
