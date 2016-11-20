from src import __main__

import unittest

class TestMain(unittest.TestCase):

    def test_no_file(self):
        self.assertFalse(__main__.main(silent = True))
        self.assertFalse(__main__.main([], silent = True))
        argv = ["Whatever"]
        self.assertFalse(__main__.main(argv, silent = True))

    def test_simple_file(self):
        argv = ["test", "tests/test_all.kc"]
        self.assertTrue(__main__.main(argv, silent = True))
