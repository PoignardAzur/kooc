from src.import_handler import ImportHandler, ImportHandlerError
from src.import_handler import _get_complete_path
from src.kooc_parser import KoocParser
from src.at_module import AtModule
from src.at_import import AtImport, KoocImportError
from src.object_list import ObjectList

from os.path import realpath

import unittest

kooc_parser = KoocParser(None)

class TestImportHandler(unittest.TestCase):
    "Tests for ImportHandler"

    def test_path_resolving_empty_wd(self):
        "Tests that relative paths are resolved with no working directory"
        self.assertEqual(
            _get_complete_path("", "tests/tests_at_import.kh"),
            realpath("tests/tests_at_import.kh")
        )

    def test_path_resolving_with_wf(self):
        "Tests that relative paths are resolved with a working file"
        self.assertEqual(
            _get_complete_path("tests/tests_all.kc", "tests_at_import.kh"),
            realpath("tests/tests_at_import.kh")
        )

    def test_path_resolving_c_files(self):
        "Tests that relative paths are resolved with a .h file"
        self.assertEqual(
            _get_complete_path("tests/tests_all.kc", "tests_at_import_c.h"),
            realpath("tests/tests_at_import_c.h")
        )

    def test_path_resolving_wrong_path(self):
        "Tests whether a wrong path raises an exception"
        # It probably doesn't? This isn't exactly an unit test

        _get_complete_path("", "file_that_doesnt_exist.kh")
        _get_complete_path("file_that", "doesnt_exist.kh")

    #TODO test _get_dir

    def test_parse_wrong_file(self):
        "Tests that passing parse_file() a wrong filename raises an exception"

        ih = ImportHandler(silent = True)
        self.assertRaises(
            ImportHandlerError,
            ih.parse_file, "", "wrong_filename.kh"
        )
        self.assertRaises(
            ImportHandlerError,
            ih.parse_file, "", "tests/test_at_import.c"
        )

    def test_parse_first_try(self):
        "Tests that parse_file() returns the right AST, and updates itself"

        ih = ImportHandler(silent = True)
        control_ast = kooc_parser.parse_file("tests/test_at_import.kh")
        self.assertEqual(
            ih.parse_file("", "tests/test_at_import.kh"),
            control_ast
        )
        self.assertEqual(
            ih._loaded_asts,
            { realpath("tests/test_at_import.kh") : control_ast }
        )

    def test_cached_ast(self):
        "Tests that parse_file() doesn't parse the same files twice"

        ih = ImportHandler(silent = True)
        ast = ih.parse_file("", "tests/test_at_import.kh")
        self.assertIs(ast, ih.parse_file("", "tests/test_at_import.kh"))


    def test_load_wrong_ast(self):
        "Tests that trying to load a unexisting AST raises an exception"

        ih = ImportHandler(silent = True)
        objs = ObjectList()
        ih.parse_file("", "tests/test_at_import.kh")
        self.assertRaises(
            KeyError,
            ih.load_objects_in, objs, "file_that", "doesnt_exist.kh"
        )

    def test_load_objects_in(self):
        "Tests simple object loading, and that files aren't loaded twice"

        ih = ImportHandler(silent = True)
        objs = ObjectList()
        ih.parse_file("", "tests/test_at_import.kh")
        self.assertTrue(ih.load_objects_in(objs, "", "tests/test_at_import.kh"))
        self.assertEqual(objs.list, [ AtModule("foobar", []) ])
        self.assertFalse(ih.load_objects_in(objs,"", "tests/test_at_import.kh"))
        self.assertEqual(objs.list, [ AtModule("foobar", []) ])
