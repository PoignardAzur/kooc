from src.mangling import mangling
from src.import_handler import ImportHandler
from src.object_list import ObjectList
from src import kooc_parser
from src.at_module import AtModule
from src.exception import KoocException
from src.at_implementation import AtImplementation

import cnorm
from pyrser.error import Diagnostic
from pyrser import error

import unittest

ih = ImportHandler(silent = True)
par = cnorm.parsing.declaration.Declaration()
kooc_parser = kooc_parser.KoocParser(ih)

module = AtModule("foo", par.parse("int x;").body, error.LocationInfo.from_stream(kooc_parser._stream))
obj_list = ObjectList()
obj_list.add_module(module)

class TestAtImplement(unittest.TestCase):
    "Unit tests for AtImplementation"

    def test_parsing_atimplement_empty(self):
        parsed_imp = kooc_parser.parse("@implementation foo {}").body[0]
        control_imp = AtImplementation("foo", [])

        self.assertEqual(parsed_imp, control_imp)

    def test_transform_atimplement_basic(self):
        imp = AtImplementation("foo", [])
        parsed_module = par.parse("int x;").body[0]
        parsed_module._name = mangling(parsed_module, "foo")

        self.assertEqual(imp.get_c_ast(obj_list), [parsed_module])
