import unittest
import os, sys
import mhi.psout

from pathlib import Path

class TestDevelPSOut(unittest.TestCase):

    def test_development(self):
        file = Path(mhi.psout.__file__)
        development_dir = Path(__file__).parents[1]
        self.assertTrue(file.is_relative_to(development_dir),
                        "Not testing development code!")

if __name__ == '__main__':
    unittest.main()
