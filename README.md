
# AMF (Argument Mining Framework)

AMF is a comprehensive toolkit designed to streamline and unify various argument mining modules into a single platform. By leveraging the Argument Interchange Format (AIF), AMF enables seamless communication between different components, including segmenters, turnators, argument relation identifiers, and argument scheme classifiers.

## Resources
- [Documentation & Tutorials](https://wiki.arg.tech/books/amf)
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
    - [Full Workflow Example](#full-workflow-example)
5. [API Reference](#api-reference)
6. [License](#license)

## Overview

AMF provides a modular approach to argument mining, integrating various components into a cohesive framework. The main features include:

- **Argument Segmentator:** Identifies and segments arguments within argumentative text.
- **Turninator:** Determines dialogue turns within conversations.
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
pip install argument-mining-framework
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

### Predictor Example

Below is an example of how to use the AMF Predictor class to generate an argument map using an input provided based on AIF:

```python
from argument_mining_framework.argument_relation.predictor import ArgumentRelationPredictor
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

In this section, we demonstrate how to use multiple components of the AMF framework in a complete argument mining workflow. This example shows how to process a text input through the Turninator, Segmenter, Propositionalizer, and Argument Relation Predictor components and  visualise the ouput.

```python
from argument_mining_framework.loader import Module


def process_pipeline(input_data):
    """Process input data through the entire pipeline."""
    # Initialize components
    turninator = load_amf_component('turninator')()
    segmenter = load_amf_component('segmenter')()
    propositionalizer = load_amf_component('propositionalizer')()    
    argument_relation = load_amf_component('argument_relation', "dialogpt", "vanila")
    visualiser = load_amf_component('visualiser')()

    # Step 1: Turninator
    turninator_output = turninator.get_turns(input_data, True)
    print(f'Turninator output: {turninator_output}')

    # Step 2: Segmenter
    segmenter_output = segmenter.get_segments(turninator_output)
    print(f'Segmenter output: {segmenter_output}')

    # Step 3: Propositionalizer
    propositionalizer_output = propositionalizer.get_propositions(segmenter_output)
    print(f'Propositionalizer output: {propositionalizer_output}')

    # Step 4: Argument Relation Prediction
    argument_map_output = argument_relation.get_argument_map(propositionalizer_output)
    print(f'Argument relation prediction output: {argument_map_output}')

    # Additional Analysis
    print("Get all claims:")
    print(argument_relation.get_all_claims(argument_map_output))
    print("===============================================")

    print("Get evidence for claim:")
    print(argument_relation.get_evidence_for_claim(
        "But this isn’t the time for vaccine nationalism", argument_map_output))
    print("===============================================")

    print("Visualise the argument map")
    visualiser.visualise(argument_map_output)

    # Initialize the converter and perform the conversion


def main():
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

    process_pipeline(input_data)

if __name__ == "__main__":
    main()
```

### Detailed Breakdown of the Workflow

1. **Turninator Component**: 
   - The Turninator processes the input text to identify and segment dialogue turns. This is particularly useful for dialogue datasets.
   - The `get_turns` method is used to perform the segmentation. The boolean parameter indicates whether the default settings should be applied.

   ```python
   turninator_output = turninator.get_turns(input_data, True)
   print(f'Turninator output: {turninator_output}')
   ```

2. **Segmenter Component**:
   - The Segmenter takes the output from the Turninator and further segments the text into argument segments.
   - This component is designed to handle various text formats and identify distinct argumentative segments within them.

   ```python
   segmenter_output = segmenter.get_segments(turninator_output)
   print(f'Segmenter output: {segmenter_output}')
   ```

3. **Propositionalizer Component**:
   - The Propositionalizer takes the segmented text and constructs propositions.

   ```python
   propositionalizer_output = propositionalizer.get_propositions(segmenter_output)
   print(f'Propositionalizer output: {propositionalizer_output}')
   ```

4. **

Argument Relation Predictor Component**:
   - The Argument Relation Predictor takes the propositions and predicts the relationships between them.
   - It can identify various types of argumentative relationships.

   ```python
   argument_map_output = argument_relation.get_argument_map(propositionalizer_output)
   print(f'Argument relation prediction output: {argument_map_output}')
   ```

5. **Visualiser Component**:
   - The Visualiser provides a visual representation of the argument map, allowing for easy interpretation of the argument structure.

   ```python
   visualiser.visualise(argument_map_output)
   ```



## License

AMF is released under the MIT License. See the `LICENSE` file for more information.

