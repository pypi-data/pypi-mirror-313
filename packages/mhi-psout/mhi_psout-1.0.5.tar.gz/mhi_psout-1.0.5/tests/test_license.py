import unittest
import datetime
import re

from pathlib import Path

class TestLicense(unittest.TestCase):

    def setUp(self):
        root = Path(__file__).parent.parent
        self.license = (root / "LICENSE").read_text()

    def test_copyright_year(self):
        m = re.search(r"Copyright (\d+)", self.license)
        self.assertIsNotNone(m)
        license_year = m.group(1)
        this_year = datetime.date.today().year
        self.assertEqual(int(license_year), this_year)

if __name__ == '__main__':
    unittest.main()
