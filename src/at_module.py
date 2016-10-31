import copy
from pyrser.parsing.node import Node

from .mangling import mangling
from .object_list import ObjectList


class AtModule(Node):

    def __init__(self, name: str, fields: list):
        self.name = name
        self.fields = fields

    def get_c_ast(self, module_list: ObjectList) :
        module_list.add_module(self)
        c_fields = copy.deepcopy(self.fields)
        for field in c_fields:
            field._name = mangling(field, field._name)
        return c_fields
