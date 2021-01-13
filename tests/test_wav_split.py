import unittest

class TestSplit(unittest.TestCase):

    def test_already_mono(self):
        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")
    def test_stereo(self):
        self.assertEqual(1,1,"This Should always work")

if __name__ == '__main__':
    unittest.main()