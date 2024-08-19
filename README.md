
# AMF (Argument Mining Framework)

AMF is a comprehensive toolkit designed to streamline and organize various argument mining modules into a unified platform. By leveraging the Argument Interchange Format (AIF), AMF facilitates seamless communication between different modules, such as argument segmentors, turnators, argument relation identifiers, and argument scheme classifiers.


## Resources
- [Documentation & Tutorials](https://amf.docs.example.com)
- [Online Demo](https://amf.demo.example.com)

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

- **Argument Segmentation:** Identifies and segments arguments within the text.
- **Turnation:** Determines dialogue turns within conversations.
- **Argument Relation Identification:** Identifies relationships between different arguments.
- **Argument Scheme Classification:** Classifies arguments based on predefined schemes.

## Installation

To install AMF, use pip to get the latest version:

```bash
pip install amf
```

## Components

### Argument Segmentor

The Argument Segmentor component is responsible for detecting and segmenting arguments within the text. It is designed to handle various text formats and structures, making it versatile for different applications.

[Read More](https://amf.docs.example.com/argument-segmentor)

### Turnator

Turninaator identifies and segments dialogue turns, making it easier to analyze conversations and interactions within texts. This module is particularly useful for dialogue-based datasets.

[Read More](https://amf.docs.example.com/turnator)

### Argument Relation Identifier

This component identifies and categorizes the argument relations between argument segments. 

[Read More](https://amf.docs.example.com/argument-relation-identifier)

### Argument Scheme Classifier

The Argument Scheme Classifier classifies arguments based on predefined schemes.

[Read More](https://amf.docs.example.com/argument-scheme-classifier)

## Usage

### Argument Relation Prediction Example

Here is a sample usage of the AMF Predictor class to perform argument mapping using the Argument Interchange Format (AIF):

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

xaif = json.dumps(xaif)
result_map = predictor.argument_map(xaif)
print(result_map)
```

## API Reference

For detailed information on all available methods and parameters, please refer to the [API Documentation](https://amf.docs.example.com/api).

## License

AMF is licensed under the [MIT License](https://opensource.org/licenses/MIT). See the LICENSE file for more details.

For more information and updates, visit the [AMF GitHub Repository](https://github.com/your-org/amf).
