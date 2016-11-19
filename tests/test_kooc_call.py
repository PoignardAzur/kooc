import cnorm
from src.mangling import mangling
from src.object_list import ObjectList
from src import kooc_parser
from src import at_module

import unittest

par = cnorm.parsing.declaration.Declaration()
kooc_parser = kooc_parser.KoocParser()

class TestKoocCall(unittest.TestCase) :

    def test_parsing(self) :

        parsed_module = kooc_parser.parse("[A.v]").body[0]
        control_module = kooc_call.KoocCall("A", "v", False, [])
        self.assertEqual(parsed_module, control_module)

        parsed_module = kooc_parser.parse("[A f]").body[0]
        control_module = kooc_call.KoocCall("A", "f", True, [])
        self.assertEqual(parsed_module, control_module)

        parsed_module = kooc_parser.parse("[A f : 4]").body[0]
        control_module = kooc_call.KoocCall("A", "f", True, [cnorm.nodes.Literal("4")])
        self.assertEqual(parsed_module, control_module)

        parsed_module = kooc_parser.parse("[A f : [A.v]]").body[0]
        control_module = kooc_call.KoocCall("A", "f", True, [kooc_parser.parse("[A.v]")])
        self.assertEqual(parsed_module, control_module)

