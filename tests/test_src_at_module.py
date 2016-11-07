import cnorm
# from src.mangling import mangling
# from src.object_list import ObjectList
from pyrser.error import Diagnostic
from src import kooc_parser
from src import at_module

import unittest

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

        # test de base
        parsed_module = kooc_parser.parse("@module foobar {int x;}")
        control_module = at_module.AtModule("foobar", par.parse("int x;").body)
        # obj_list = ObjectList()
        # to_check = par.parse("int a = 3;").body[0]
        # to_check._name = mangling(to_check, "foo")
        self.assertEqual(parsed_module, control_module)








        # par = cnorm.parsing.declaration.Declaration()

        
        # # tester sans arg
        # mod = at_module.AtModule("foo", [])
        # obj_list = ObjectList()
        # to_check = par.parse(str())
        # self.assertEqual(mod.get_c_ast(obj_list), to_check.body)

        # # tester sans nom
        # # mod = at_module.AtModule(str(), par.parse("int a = 3;").body)
        # self.assertRaises(TypeError, at_module.AtModule(str(), par.parse("int a = 3;").body))
        # # obj_list = ObjectList()
        # # to_check = par.parse(str())
        # # self.assertEqual(mod.get_c_ast(obj_list), to_check.body)

        # # tester avec un int
        # mod = at_module.AtModule("foo", par.parse("int a = 3;").body)
        # obj_list = ObjectList()
        # to_check = par.parse("int a = 3;").body[0]
        # to_check._name = mangling(to_check, "foo")
        # self.assertEqual(mod.get_c_ast(obj_list), [to_check])
