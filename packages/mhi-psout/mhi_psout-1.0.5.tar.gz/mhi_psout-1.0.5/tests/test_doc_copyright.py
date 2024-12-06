import unittest
import datetime
import re

from pathlib import Path

REGEX = r"""copyright\s*=\s*['"](\d+), Manitoba Hydro International Ltd\.['"]"""

class TestDocCopyright(unittest.TestCase):

    def setUp(self):
        root = Path(__file__).parent.parent
        self.conf = (root / 'docs' / 'source' / 'conf.py').read_text()

    def test_copyright_year(self):
        m = re.search(REGEX, self.conf)
        self.assertIsNotNone(m)
        license_year = m.group(1)
        this_year = datetime.date.today().year
        self.assertEqual(int(license_year), this_year)

if __name__ == '__main__':
    unittest.main()
