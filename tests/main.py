from src import main

import unittest

class TestMain(unittest.TestCase):

    def test_no_file(self):
        self.assertFalse(main.main())
        self.assertFalse(main.main([]))
        argv = ["Whatever"]
        self.assertFalse(main.main(argv))

    def test_simple_file(self):
        argv = ["test", "tests/test.kc"]
        self.assertTrue(main.main(argv))
