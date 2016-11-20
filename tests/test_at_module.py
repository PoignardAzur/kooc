from src.mangling import mangling
from src.import_handler import ImportHandler
from src.object_list import ObjectList
from src import kooc_parser
from src.at_module import AtModule, AtModuleError

import cnorm
from pyrser.error import Diagnostic

import unittest

ih = ImportHandler()
par = cnorm.parsing.declaration.Declaration()
kooc_parser = kooc_parser.KoocParser(ih)

class TestAtModule(unittest.TestCase):
    "Unit tests for AtModule"

    def test_parsing_empty(self):
        "Test parsing empty module"
        parsed_module = kooc_parser.parse("@module foo {}").body[0]
        control_module = AtModule("foo", [])
        self.assertEqual(parsed_module, control_module)

    def test_parsing_error(self):
        "Test incorrect syntaxes"
        self.assertRaises(Diagnostic, kooc_parser.parse, "@module {}")
        self.assertRaises(Diagnostic, kooc_parser.parse, "@module")
        self.assertRaises(Diagnostic, kooc_parser.parse, '@module "bar" {}')

    def test_module_base(self):
        "Test parsing simple modules"
        self.assertEqual(
            kooc_parser.parse("@module foobar {int x;}"),
            AtModule("foobar", par.parse("int x;").body)
        )
        parsed_module = kooc_parser.parse("""
            @module foobar_one {
                int x;
                int x;
            }
        """)
        control_module = AtModule(
            "foobar_one",
            par.parse("int x; int x;").body
        )
        self.assertEqual(parsed_module, control_module)

    def test_transform_empty(self):
        "Test transforming empty module"

        obj_list = ObjectList()
        module = AtModule("foo", [])
        self.assertEqual(module.get_c_ast(obj_list), [])

    def test_transform_int(self):
        "Test transforming module with single declaration"

        obj_list = ObjectList()

        control_module = AtModule("bar", par.parse("int x;").body)
        parsed_module = par.parse("int x;").body[0]
        parsed_module._name = mangling(parsed_module, "bar")
        self.assertEqual(control_module.get_c_ast(obj_list), [parsed_module])

    def test_transform_moreints(self):
        obj_list = ObjectList()

        # test avec plus d'ints
        control_module = AtModule("foobar", par.parse("int x; int y; int z;").body)
        parsed_module = par.parse("int x; int y; int z;").body
        for parsed in parsed_module:
            parsed._name = mangling(parsed, "foobar")
        self.assertEqual(control_module.get_c_ast(obj_list), parsed_module)

    def test_error_samemodules(self):
        obj_list = ObjectList()

        # test multi-module avec le même nom
        AtModule("foo", []).get_c_ast(obj_list)
        t1 = AtModule("foo", [])
        self.assertRaises(AtModuleError, t1.get_c_ast, obj_list)

    def test_error_samevariables(self):
        obj_list = ObjectList()

        # test variable avec le même mangling
        t2 = AtModule("bar", par.parse("int x; int x;").body)
        self.assertRaises(AtModuleError, t2.get_c_ast, obj_list)
        t3 = AtModule("foobar", par.parse("int x; static int x;").body)
        self.assertRaises(AtModuleError, t3.get_c_ast, obj_list)

    def test_error_implementedfunctions(self):
        obj_list = ObjectList()

        # test fonctions implémentées
        t4 = AtModule("foobaar", par.parse("int x() {return (2);}").body)
        self.assertRaises(AtModuleError, t4.get_c_ast, obj_list)

        # dégager les variables statics
        # t3 = AtModule("foobar", par.parse("int x; static int x;").body)
        # self.assertRaises(AtModuleError, t3.get_c_ast, obj_list)
