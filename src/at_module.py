import copy
from pyrser.parsing.node import Node

from .mangling import mangling
from .object_list import ObjectList


class AtModuleErrorMultiModule(Exception):
    pass

class AtModuleErrorMultiObj(Exception):
    pass

class AtModule(Node):

    def __init__(self, name: str, fields: list):
        self.name = name
        self.fields = fields

    def get_c_ast(self, module_list: ObjectList) :
        check = list()
        for ob_list in module_list.list:
            if self.name == ob_list.name:
                raise AtModuleErrorMultiModule
        module_list.add_module(self)
        c_fields = copy.deepcopy(self.fields)
        for field in c_fields:
            field._name = mangling(field, field._name)
            if field._name in check:
                raise AtModuleErrorMultiObj
            check.append(field._name)
        return c_fields
