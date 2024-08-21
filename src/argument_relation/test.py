import json


def is_json(input_data):
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
# Example usage
input_data = {"key": "value"}  # or 'Just some text'
#input_data = "this is sample data"
if is_json(input_data):
    print("Input data is JSON.")
else:
    print("Input data is a plain string.")
