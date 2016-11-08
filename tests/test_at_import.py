from src.at_import import AtImport, KoocImportError
from src.at_module import AtModule
from src.kooc_parser import KoocParser
from src.object_list import ObjectList

import unittest

from pyrser.error import Diagnostic
from cnorm.parsing.declaration import Declaration

kooc_parser = KoocParser()
c_parser = Declaration()

class TestAtImport(unittest.TestCase):
    "Tests for @import"

    def test_parse_import(self):
        "Tests the parsing from KOOC text to KOOC AST"

        self.assertEqual(
            kooc_parser.parse('@import "test_at_import.kh"').body,
            [AtImport("test_at_import.kh")]
        )
        self.assertRaises(
            KoocImportError,
            kooc_parser.parse,
            '@import "test_at_import.kh"'
        )
        self.assertRaises(Diagnostic, kooc_parser.parse, '@import filename')
        self.assertRaises(Diagnostic, kooc_parser.parse, '@import;')

    def test_get_c_ast(self):
        "Tests that the node is correctly transformed"

        objects = ObjectList()

        self.assertRaises(
            KoocImportError,
            AtImport("wrong_file_name.kh").get_c_ast, ObjectList()
        )
        self.assertEqual(
            AtImport("test_at_import.kh").get_c_ast(objects),
            c_parser.parse("""
                #ifndef TEST_AT_IMPORT_H_
                # define TEST_AT_IMPORT_H_
                # include test_at_import.h
                #endif /* !TEST_AT_IMPORT_H_ */
            """).body
        )
        self.assertEqual(objects.list, [ AtModule("foobar", []) ])

    def test_remember_c_types(self):
        "Tests that types declared in imported files are known to the parser"

        self.assertEqual(
            kooc_parser.parse('@import "test_at_import.kh" CustomType x;').body[4],
            kooc_parser.parse('typedef int CustomType; CustomType x;').body[1]
        )
