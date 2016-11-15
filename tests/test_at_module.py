import cnorm
from src.at_module import AtModuleErrorMultiModule
from src.at_module import AtModuleErrorMultiObj
from src.mangling import mangling
from src.object_list import ObjectList
from pyrser.error import Diagnostic
from src import kooc_parser
from src import at_module

import unittest

par = cnorm.parsing.declaration.Declaration()
kooc_parser = kooc_parser.KoocParser()

class TestAtModule(unittest.TestCase):

    def test_parsing(self):

        # test sans arg
        parsed_module = kooc_parser.parse("@module foo {}").body[0]
        control_module = at_module.AtModule("foo", [])
        self.assertEqual(parsed_module, control_module)

        # test sans nom
        self.assertRaises(Diagnostic, kooc_parser.parse, "@module {}")
        self.assertRaises(Diagnostic, kooc_parser.parse, "@module")
        self.assertRaises(Diagnostic, kooc_parser.parse, '@module "bar" {}')

        # tests de base
        parsed_module = kooc_parser.parse("@module foobar {int x;}")
        control_module = at_module.AtModule("foobar", par.parse("int x;").body)
        self.assertEqual(parsed_module, control_module)

        parsed_module1 = kooc_parser.parse("""
        @module foobar_one {int x;
        int x;
        }
        """)
        control_module1 = at_module.AtModule("foobar_one", par.parse("int x; int x;").body)
        self.assertEqual(parsed_module1, control_module1)

    def test_transfo(self):
        obj_list = ObjectList()

        # test sans arg
        control_module = at_module.AtModule("foo", [])
        parsed_module = par.parse("")
        self.assertEqual(control_module.get_c_ast(obj_list), parsed_module.body)

        # tester avec un int
        control_module = at_module.AtModule("bar", par.parse("int x;").body)
        parsed_module = par.parse("int x;").body[0]
        parsed_module._name = mangling(parsed_module, "bar")
        self.assertEqual(control_module.get_c_ast(obj_list), [parsed_module])

        control_module = at_module.AtModule("foobar", par.parse("int x; int y; int z;").body)
        parsed_module = par.parse("int x; int y; int z;").body
        for parsed in parsed_module:
            parsed._name = mangling(parsed, "foobar")
        self.assertEqual(control_module.get_c_ast(obj_list), parsed_module)


    def test_error(self):
        obj_list = ObjectList()

        # test multi-module avec le même nom
        at_module.AtModule("foo", []).get_c_ast(obj_list)
        t1 = at_module.AtModule("foo", [])
        self.assertRaises(AtModuleErrorMultiModule, t1.get_c_ast, obj_list)

        # test variable avec le même mangling
        t2 = at_module.AtModule("bar", par.parse("int x; int x;").body)
        self.assertRaises(AtModuleErrorMultiObj, t2.get_c_ast, obj_list)

        t3 = at_module.AtModule("foobar", par.parse("int x; static int x;").body)
        self.assertRaises(AtModuleErrorMultiObj, t3.get_c_ast, obj_list)
