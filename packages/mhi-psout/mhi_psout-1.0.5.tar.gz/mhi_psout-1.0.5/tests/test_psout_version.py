import unittest
import os, sys
from pathlib import Path
from mhi.psout import __version__ as VERSION, __version_hex__ as VERSION_HEX

class TestPSoutVersion(unittest.TestCase):

    def setUp(self):
        major, minor, patch, extra = VERSION_HEX.to_bytes(4, 'big')
        release_type = hex(extra >> 4)[2:]
        release = extra & 15

        self.assertIn(release_type, 'abcf', "Invalid release type")

        version = "{:d}.{:d}.{:d}".format(major, minor, patch)
        self.version_mmp = version
    
        if release_type == 'a':
            version += f"a{release}"
        elif release_type == 'b':
            version += f"b{release}"
        elif release_type == 'c':
            version += f"rc{release}"
        elif release > 0:
            version += f"p{release}"

        self.major = major
        self.minor = minor
        self.patch = patch
        self.extra = extra
        self.version = version
        self.release_type = release_type
        self.release = release
        
    
    def test_version(self):
        release_type = self.release_type

        self.assertEqual(self.version, VERSION,
                         "VERSION & VERSION_HEX do not match")             

    def test_release_notes(self):
        root = Path(__file__).parent.parent
        version = self.version_mmp if self.release_type != 'p' else self.version
        with open(root / "docs" / "source" / "changes.rst") as file:
            versions = [line.strip() for line in file
                        if len(line) <= 12 and '.' in line and ' ' not in line]
        found = any(ver == version for ver in versions)
        latest = versions[0] if versions else "-none-"

        self.assertTrue(found,
                        f"Version {version!r} not found in release notes")

        self.assertEqual(version, latest,
                        f"Version {version!r} not latest in release notes")
        
        

if __name__ == '__main__':
    unittest.main()
