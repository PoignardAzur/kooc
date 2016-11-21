import cnorm
from src.mangling import mangling
from src.import_handler import ImportHandler
from src.kooc_parser import KoocParser
from src.object_list import ObjectList
from src import kooc_parser
from src import at_module
from src import kooc_call

import unittest

c_parser = cnorm.parsing.declaration.Declaration()
ih = ImportHandler(silent = True)
kooc_parser = KoocParser(ih)

class TestKoocCall(unittest.TestCase) :

    liste = ObjectList()
    pa = kooc_parser.parse("""@module A{int d; long v; int f(); int f(int);}""")
    for module in pa.body :
        liste.add_module(module)

    def compare_call(self, a,b, num):
        self.assertEqual(a.module_name, b.module_name)
        self.assertEqual(a.name, b.name)
        self.assertEqual(a.isFunc, b.isFunc)


    def test_var(self) :
        parsed_module = kooc_parser.parse("[A.d];", "kooc_call")
        control_module = kooc_call.KoocCall("A", "d", "", False, None)
        self.compare_call(parsed_module, control_module, "test_parsing0")
        self.assertEqual(parsed_module.get_c_ast(self.liste).to_c(), control_module.get_c_ast(self.liste).to_c())
        parsed_module = kooc_parser.parse("@!(long)[A.v];", "kooc_call")
        control_module = kooc_call.KoocCall("A", "v", "long", False, None)
        self.compare_call(parsed_module, control_module, "test_parsing4")
        self.assertEqual(parsed_module.get_c_ast(self.liste).to_c(), control_module.get_c_ast(self.liste).to_c())


    def test_function(self):
        parsed_module = kooc_parser.parse("[A f];", "kooc_call")
        control_module = kooc_call.KoocCall("A", "f", "", True, [])
        self.compare_call(parsed_module, control_module, "test_parsing1")
        #self.assertEqual(parsed_module.get_c_ast(self.liste).to_c(), control_module.get_c_ast(self.liste).to_c())

    def test_test(self):
        parsed_module = kooc_parser.parse("[A f : 4];", "kooc_call")
        control_module = kooc_call.KoocCall("A", "f", "", True, ['4'])
        self.compare_call(parsed_module, control_module, "test_parsing2")
        #self.assertEqual(parsed_module.get_c_ast(self.liste).to_c(), control_module.get_c_ast(self.liste).to_c())

        parsed_module = kooc_parser.parse("[A f : [A.v]];", "kooc_call")
        control_module = kooc_call.KoocCall("A", "f", "", True, [kooc_parser.parse("[A.v];", "kooc_call")])
        self.compare_call(parsed_module, control_module, "test_parsing3")
        #self.assertEqual(parsed_module.get_c_ast(self.liste).to_c(), control_module.get_c_ast(self.liste).to_c())
