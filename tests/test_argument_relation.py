import unittest
from amf.src.argument_mining_framework.loader import Module

class TestArgumentRelation(unittest.TestCase):
    def setUp(self):
        self.argument_relation = Module('argument_relation', 'dialogpt', 'vanila')

    def test_argument_relation_output(self):
        input_data = {"AIF": "sample AIF data"}
        output = self.argument_relation.get_argument_map(input_data)
        self.assertIsInstance(output, dict)
        self.assertIn('AIF', output)

if __name__ == '__main__':
    unittest.main()
