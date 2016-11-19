import copy
import sys
from pyrser.parsing.node import Node

from .mangling import mangling
from .object_list import ObjectList


class AtImplementation(Node):

    def __init__(self, name: str, fields: list):
        self.name = name
        self.fields = fields

    def get_c_ast(self, module_list: ObjectList) :
        # TODO
        for elt in ObjectList.list
            if elt.name == self.name
                ast = copy.deepcopy(elt)
                ast.append(ast, self.fields)
                for field in ast
                    field._name = mangling(field, field._name)
                return ast
        sys.stderr.write("Error in AtImplementation.get_c_ast\n")
        return []
