import requests
import json
import io
from IPython.display import display, SVG
import webbrowser
import tempfile
import os

class JsonToSvgConverter:
    def __init__(self, url):
        self.url = url

    def convert(self, json_data):
        try:
            # Convert JSON data to a binary file-like object
            json_bytes = json.dumps(json_data).encode('utf-8')
            json_file_like = io.BytesIO(json_bytes)
            print(json_file_like)

            # Prepare the files dictionary to mimic file upload
            files = {'file': ('input.json', json_file_like, 'application/json')}

            # Send the POST request
            response = requests.post(self.url, files=files)
            print(response)
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

# Example usage
if __name__ == "__main__":
    #url = 'http://svg.amfws.arg.tech'
    url = 'http://ws.arg.tech/t/json-svg'

    json_data = {
        'AIF': {
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
        },
        'ova': {},
        'dialog': {},
        'text': {'txt': 'Liam Halligan... Fiona Bruce...'}
    }

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

    converter = JsonToSvgConverter(url)
    svg_output = converter.convert(json_data)
    if svg_output:
        converter.visualize_svg(svg_output)
