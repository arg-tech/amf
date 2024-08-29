import unittest
from src.argument_mining_framework.loader import Module

class TestSegmenter(unittest.TestCase):
    def setUp(self):
        self.segmenter = Module('segmenter')

    def test_segmenter_output(self):
        input_data = {"AIF": "sample AIF data"}
        output = self.segmenter.get_segments(input_data)
        self.assertIsInstance(output, dict)
        self.assertIn('AIF', output)

if __name__ == '__main__':
    unittest.main()
