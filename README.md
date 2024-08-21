
# AMF (Argument Mining Framework)

AMF is a comprehensive toolkit designed to streamline and unify various argument mining modules into a single platform. By leveraging the Argument Interchange Format (AIF), AMF enables seamless communication between different components, including segmenters, turnators, argument relation identifiers, and argument scheme classifiers.

## Resources
- [Documentation & Tutorials](https://amf.docs.example.com)
- [Online Demo](https://n8n.arg.tech/workflow/2)

## Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [Components](#components)
    - [Argument Segmentor](#argument-segmentor)
    - [Turnator](#turnator)
    - [Argument Relation Identifier](#argument-relation-identifier)
    - [Argument Scheme Classifier](#argument-scheme-classifier)
4. [Usage](#usage)
    - [Predictor Example](#predictor-example)
5. [API Reference](#api-reference)
6. [License](#license)

## Overview

AMF provides a modular approach to argument mining, integrating various components into a cohesive framework. The main features include:

- **Argument Segmentation:** Identifies and segments arguments within argumentative text.
- **Turnation:** Determines dialogue turns within conversations.
- **Argument Relation Identification:** Identifies argument relationships between argument units.
- **Argument Scheme Classification:** Classifies arguments based on predefined schemes.

## Installation

### Prerequisites

Ensure you have Python installed on your system. AMF is compatible with Python 3.6 and above.

### Step 1: Create a Virtual Environment

It's recommended to create a virtual environment to manage dependencies:

```bash
python -m venv amf-env
```

Activate the virtual environment:

- **Windows:**
  ```bash
  .\amf-env\Scripts\activate
  ```
- **macOS/Linux:**
  ```bash
  source amf-env/bin/activate
  ```

### Step 2: Install Dependencies

With the virtual environment activated, install AMF using pip:

```bash
pip install amf
```

This command will install the latest version of AMF along with its dependencies.

## Components

### Argument Segmentor

The Argument Segmentor component is responsible for detecting and segmenting arguments within text. 

[Read More](http://default-segmenter.amfws.arg.tech/segmenter-01)

### Turnator

The Turnator identifies and segments dialogue turns, facilitating the analysis of conversations and interactions within texts. This module is particularly useful for dialogue-based datasets.

[Read More](http://default-turninator.amfws.arg.tech/turninator-01)

### Argument Relation Identifier

This component identifies and categorizes the relationships between argument units.

[Read More](http://bert-te.amfws.arg.tech/bert-te)

### Argument Scheme Classifier

The Argument Scheme Classifier categorizes arguments based on predefined schemes, enabling structured argument analysis.

[Read More](http://amf-schemes.amfws.arg.tech)

## Usage

### Argument Relation Prediction Example

Below is an example of how to use the AMF Predictor class to generate argument map using an input provided based on  AIF:

```python
from amf import ArgumentRelationPredictor
import json

# Initialize Predictor
predictor = ArgumentRelationPredictor(model_type="dialogpt", variant="vanilla")

# Example XAIF structure
xaif = {
    "AIF": {
        "nodes": [
            {"nodeID": "1", "text": "THANK YOU", "type": "I", "timestamp": "2016-10-31 17:17:34"},
            {"nodeID": "2", "text": "COOPER : THANK YOU", "type": "L", "timestamp": "2016-11-10 18:34:23"},
            # Add more nodes as needed
        ],
        "edges": [
            {"edgeID": "1", "fromID": "1", "toID": "20", "formEdgeID": "None"},
            {"edgeID": "2", "fromID": "20", "toID": "3", "formEdgeID": "None"}
            # Add more edges as needed
        ],
        "locutions": [],
        "participants": []
    },
    "text": "people feel that they have been treated disrespectfully..."
}

# Convert XAIF structure to JSON string
xaif_json = json.dumps(xaif)

# Predict argument relations
result_map = predictor.argument_map(xaif_json)
print(result_map)
```

### Full Workflow Example

In this section, we demonstrate how to use multiple components of the AMF framework in a complete argument mining workflow. This example shows how to process a text input through the Turninator, Segmenter, Propositionalizer, and Argument Relation Predictor components.

```python
import json
from src.argument_relation.predictor import ArgumentRelationPredictor as ArgumentRelation
from src.turninator.turninator import Turninator
from src.segmenter.segmenter import Segmenter
from src.propositionaliser.propositionalizer import Propositionalizer

def main():
    # Initialize components
    turninator = Turninator()
    segmenter = Segmenter()
    propositionalizer = Propositionalizer()
    predictor = ArgumentRelation("dialogpt", "vanilla")

    # Sample input data
    input_data = (
        """Liam Halligan: Vaccines mark a major advance in human achievement since the """
        """enlightenment into the 19th Century and Britain’s been at the forefront of """
        """those achievements over the years and decades. But this isn’t the time for """
        """vaccine nationalism. I agree we should congratulate all the scientists, those """
        """in Belgium, the States, British scientists working in international teams here """
        """in the UK, with AstraZeneca.\n"""
        """Fiona Bruce: What about the logistical capabilities? They are obviously """
        """forefront now, now we’ve got a vaccine that’s been approved. It’s good -- I’m """
        """reassured that the British Army are going to be involved. They’re absolute world """
        """experts at rolling out things, complex logistic capabilities. This is probably """
        """going to be the biggest logistical exercise that our armed forces have undertaken """
        """since the Falklands War, which I’m old enough to remember, just about. So, as a """
        """neutral I’d like to see a lot of cross-party cooperation, and I’m encouraged with """
        """Sarah’s tone, everybody wants to see us getting on with it now. They don’t want """
        """to see competition on whose vaccine is best. There will be some instances where """
        """the Pfizer vaccine works better, another where you can’t have cold refrigeration, """
        """across the developing world as well, a cheaper vaccine like the AstraZeneca works """
        """better. Let’s keep our fingers crossed and hope we make a good job of this."""
    )

    # Process input through each component
    turninator_output = turninator.turninator_default(input_data, True)
    print(f'Turninator output: {turninator_output}')

    segmenter_output = segmenter.segmenter_default(turninator_output)
    print(f'Segmenter output: {segmenter_output}')

    propositionalizer_output = propositionalizer.propositionalizer_default(segmenter_output)
    print(f'Propositionalizer output: {propositionalizer_output}')

    argument_map_output = predictor.argument_map(propositionalizer_output)
    print(f'Argument relation prediction output: {argument_map_output}')

if __name__ == "__main__":
    main()
```

### Detailed Breakdown of the Workflow

1. **Turninator Component**: 
   - The Turninator processes the input text to identify and segment dialogue turns. This is particularly useful for dialogue datasets.
   - The `turninator_default` method is used to perform the segmentation. The boolean parameter indicates whether the default settings should be applied.

   ```python
   turninator_output = turninator.turninator_default(input_data, True)
   print(f'Turninator output: {turninator_output}')
   ```

2. **Segmenter Component**:
   - The Segmenter takes the output from the Turninator and further segments the text into argument segments.
   - This component is designed to handle various text formats and identify distinct argumentative segments within them.

   ```python
   segmenter_output = segmenter.segmenter_default(turninator_output)
   print(f'Segmenter output: {segmenter_output}')
   ```

3. **Propositionalizer Component**:
   - The Propositionalizer takes the segmented text and contructs propositions.
   ```python
   propositionalizer_output = propositionalizer.propositionalizer_default(segmenter_output)
   print(f'Propositionalizer output: {propositionalizer_output}')
   ```

4. **Argument Relation Predictor**:
   - The Argument Relation Predictor analyzes the propositions and identifies the argument relationships between them. The argument relations include support, contradiction, or rephrase.

   ```python
   argument_map_output = predictor.argument_map(propositionalizer_output)
   print(f'Argument relation prediction output: {argument_map_output}')
   ```

### Customization and Advanced Usage

- **Model Selection**: You can customize the `model_type` and `variant` parameters in the `ArgumentRelationPredictor` to use different models or configurations, depending on your specific requirements.

- **Handling Complex Inputs**: The framework is flexible and can be extended to handle more complex inputs or additional pre-processing steps, making it suitable for a wide range of argument mining tasks.

```


## API Reference

For detailed information on all available methods and parameters, please refer to the [API Documentation](https://amf.docs.example.com/api).

## License

AMF is licensed under the [MIT License](https://opensource.org/licenses/MIT). For more details, please refer to the LICENSE file.


