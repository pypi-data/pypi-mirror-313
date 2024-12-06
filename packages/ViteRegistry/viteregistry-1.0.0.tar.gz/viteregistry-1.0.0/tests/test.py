import unittest
from ViteRegistry.core import *


class TestViteRegistry(unittest.TestCase):

    def test(self):
        result = read_registry('HKEY_LOCAL_MACHINE', "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\DefaultProductKey", "ProductId")
        print(result)


if __name__ == '__main__':
    unittest.main()
