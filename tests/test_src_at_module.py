import cnorm
from src.mangling import mangling
from src.object_list import ObjectList
from src import at_module

import unittest

class TestAtModule(unittest.TestCase):

    def test_new_module(self):
        # tester

        # tester avec un int
        par = cnorm.parsing.declaration.Declaration()
        mod = at_module.AtModule("foo", par.parse("int a = 3;").body)
        obj_list = ObjectList()
        to_check = par.parse("int a = 3;").body[0]
        to_check._name = mangling(to_check, "foo")
        self.assertEqual(mod.get_c_ast(obj_list), [to_check])
