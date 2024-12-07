import unittest
from nmtextprocessor1 import remove_stop_words

class TestNMTextProcessor(unittest.TestCase):
    def test_remove_stop_words(self):
        text = "I have been going to the market It has been raining"
        expected = "I been going to the market It been raining"
        self.assertEqual(remove_stop_words(text), expected)
if __name__ == "__main__":
    unittest.main()