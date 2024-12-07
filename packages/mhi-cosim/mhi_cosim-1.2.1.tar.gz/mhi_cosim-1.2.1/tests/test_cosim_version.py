import unittest
from mhi.cosim import VERSION, VERSION_HEX

class TestVersion(unittest.TestCase):
    
    def test_version(self):
        major, minor, patch, extra = VERSION_HEX.to_bytes(4, 'big')
        version = "{:x}.{:x}.{:x}".format(major, minor, patch)
        release_type = hex(extra >> 4)[2:]
        release = extra & 15
        
        self.assertIn(release_type, 'abcf', "Invalid release type")

        if release_type == 'a':
            version += f"a{release}"
        elif release_type == 'b':
            version += f"b{release}"
        elif release_type == 'c':
            version += f"rc{release}"
        elif release > 0:
            version += f"p{release}"

        self.assertEqual(version, VERSION, "VERSION & VERSION_HEX do not match")             

if __name__ == '__main__':
    unittest.main()
