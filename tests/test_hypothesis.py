import unittest
from src.argument_mining_framework.loader import Module

class TestHypothesis(unittest.TestCase):
    def setUp(self):
        # Initialize the hypothesis module with specific model and variant
        self.hypothesis = Module('hypothesis', 'roberta', 'vanila')

    def test_hypothesis_output(self):
        # Example input data for sequence classification
        input_data = ["Sample premise", "Sample hypothesis"]

        # Get the prediction output from the hypothesis module
        output = self.hypothesis.predict(input_data)
        print(output)  # For debugging purposes

        # Check if the output is a tuple with exactly three elements
        self.assertIsInstance(output, tuple)
        self.assertEqual(len(output), 3)

        # Extract the lists from the tuple
        labels, scores1, scores2 = output

        # Validate labels
        self.assertIsInstance(labels, list)
        self.assertGreater(len(labels), 0)
        for label in labels:
            self.assertIsInstance(label, str)

        # Validate first set of scores
        self.assertIsInstance(scores1, list)
        self.assertEqual(len(scores1), len(labels))  # Ensure scores match number of labels
        for score in scores1:
            self.assertIsInstance(score, float)

        # Validate second set of scores
        self.assertIsInstance(scores2, list)
        self.assertEqual(len(scores2), len(labels))  # Ensure scores match number of labels
        for score in scores2:
            self.assertIsInstance(score, float)

if __name__ == '__main__':
    unittest.main()
