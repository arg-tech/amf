import unittest
from amf.src.argument_mining_framework.loader import Module

class TestTurninator(unittest.TestCase):
    def setUp(self):
        self.turninator = Module('turninator')

    def test_turninator_output(self):
        input_data = "Sample input text for turninator."
        output = self.turninator.get_turns(input_data, True)
        self.assertIsInstance(output, dict)
        self.assertIn('AIF', output)

if __name__ == '__main__':
    unittest.main()
