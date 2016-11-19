from src import __main__

import unittest

class TestMain(unittest.TestCase):

    def test_no_file(self):
        self.assertFalse(__main__.main())
        self.assertFalse(__main__.main([]))
        argv = ["Whatever"]
        self.assertFalse(__main__.main(argv))

    def test_simple_file(self):
        argv = ["test", "tests/test_all.kc"]
        self.assertTrue(__main__.main(argv))
