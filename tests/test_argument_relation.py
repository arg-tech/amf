import unittest
import sys
import os

# Add the path to the `amf` directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'amf')))

from amf.src.argument_relation.predictor import ArgumentRelationPredictor

class TestArgumentRelationPredictor(unittest.TestCase):
    def setUp(self):
        self.predictor = ArgumentRelationPredictor("dialogpt", "vanila")

    def test_prediction(self):
        test_data = "Sample input text"
        predictions, confidence, probabilities = self.predictor.predict(test_data)
        self.assertIsInstance(predictions, list)
        self.assertIsInstance(confidence, list)

if __name__ == '__main__':
    unittest.main()
