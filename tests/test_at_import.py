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

        ast_body = kooc_parser.parse('@import "tests/test_at_import.kh"').body
        self.assertEqual(
            ast_body,
            [ AtImport("tests/test_at_import.kh", kooc_parser) ]
        )
        self.assertEqual(
            ast_body[0].ast,
            kooc_parser.parse_file("tests/test_at_import.kh")
        )

        ast_body = kooc_parser.parse('@import "tests/test_at_import_c.h"').body
        self.assertEqual(
            ast_body,
            [ AtImport("tests/test_at_import_c.h", kooc_parser) ]
        )
        self.assertEqual(
            ast_body[0].ast,
            c_parser.parse_file("tests/test_at_import_c.h")
        )
        self.assertRaises(
            KoocImportError,
            kooc_parser.parse, '@import "test_incorrect_import_c.h"'
        )

        self.assertRaises(
            KoocImportError,
            kooc_parser.parse, '@import "wrong_file_name.kh"'
        )
        self.assertRaises(
            Diagnostic,
            kooc_parser.parse, "@import 'tests/test_at_import.kh'"
        )
        self.assertRaises(KoocImportError, kooc_parser.parse, '@import "aaa"')
        self.assertRaises(Diagnostic, kooc_parser.parse, '@import filename')
        self.assertRaises(Diagnostic, kooc_parser.parse, '@import;')

    def test_get_c_ast(self):
        "Tests that the node is correctly transformed"

        objs = ObjectList()

        c_ast = AtImport("tests/test_at_import.kh", kooc_parser).get_c_ast(objs)
        control_ast = c_parser.parse("""
            #ifndef TEST_AT_IMPORT_H_
            # include "tests/test_at_import.h"
            # define TEST_AT_IMPORT_H_
            #endif /* !TEST_AT_IMPORT_H_ */
        """)
        self.assertEqual(len(c_ast), 4)
        for i in range(0, 4):
            self.assertEqual(c_ast[i].value, control_ast.body[i].value)

        self.assertEqual(objs.list, [ AtModule("foobar", []) ])

    def test_remember_c_types(self):
        "Tests that types declared in imported files are known to the parser"

        parse = kooc_parser.parse
        self.assertEqual(
            parse('@import "tests/test_at_import.kh" CustomType x;').body[1],
            c_parser.parse('typedef int CustomType; CustomType x;').body[1]
        )
        self.assertEqual(
            parse('@import "tests/test_at_import.h" CustomType2 x;').body[1],
            c_parser.parse('typedef int CustomType2; CustomType2 x;').body[1]
        )

    def test_import_protection(self):
        "Tests that import is protected against double inclusion"

        kooc_parser.parse_file('tests/test_double_import.kh')
