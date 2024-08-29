import unittest
from amf.src.argument_mining_framework.loader import Module

class TestPropositionalizer(unittest.TestCase):
    def setUp(self):
        self.propositionalizer = Module('propositionalizer')

    def test_propositionalizer_output(self):
        input_data = {"AIF": "sample AIF data"}
        output = self.propositionalizer.get_propositions(input_data)
        self.assertIsInstance(output, dict)
        self.assertIn('AIF', output)

if __name__ == '__main__':
    unittest.main()
