import unittest
from src.argument_mining_framework.loader import Module

class TestScheme(unittest.TestCase):
    def setUp(self):
        # Initialize the scheme module with specific model and variant
        self.scheme = Module('scheme', 'roberta', 'vanila')

    def test_scheme_output(self):
        # Example input data for sequence classification
        input_data = ["Sample premise", "Sample scheme"]

        # Get the prediction output from the scheme module
        output = self.scheme.predict(input_data)

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
