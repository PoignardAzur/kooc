import copy
from pyrser.parsing.node import Node
from mangling import mangling


class AtImplementation(Node):

    def __init__(self, name: str, fields: list):
        self.name = name
        self.fields = fields

    def get_c_ast(self, module_list: object_list) :
        # TODO
        return []
