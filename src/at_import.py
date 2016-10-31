from pyrser.parsing.node import Node

from .mangling import mangling
from .object_list import ObjectList

class AtImport(Node):

    def __init__(self, filename: str):
        self.filename = filename

    def get_c_ast(self, module_list: ObjectList) :
        # TODO
        return []
