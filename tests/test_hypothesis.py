import unittest
from amf.src.argument_mining_framework.loader import Module

class TestHypothesis(unittest.TestCase):
    def setUp(self):
        # Initialize the hypothesis module with specific model and variant
        self.hypothesis = Module('hypothesis', 'roberta', 'vanila')

    def test_hypothesis_output(self):
        # Example input data for sequence classification
        input_data = ["Sample premise", "Sample hypothesis"]

        # Get the prediction output from the hypothesis module
        output = self.hypothesis.predict(input_data)

        # Check if the output is a list
        self.assertIsInstance(output, list)
        
        # Ensure that the list contains at least one item
        self.assertGreater(len(output), 0)

        # Check that each item in the list is a dictionary with specific keys
        for result in output:
            self.assertIsInstance(result, dict)
            self.assertIn('label', result)
            self.assertIn('score', result)

            # Check that the 'label' is a string and 'score' is a float
            self.assertIsInstance(result['label'], str)
            self.assertIsInstance(result['score'], float)

if __name__ == '__main__':
    unittest.main()
