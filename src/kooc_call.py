from pyrser.parsing.node import Node

from .mangling import mangling
from .object_list import ObjectList

class KoocCall(Node):

    def __init__(self, module_name: str, name: str, isFunc = False, args = []):
        #args: List<cnorm.nodes.Expr>
        self.module_name = module_name
        self.name = name
        self.isFunc = isFunc
        self.args = args

    def get_c_ast(self, module_list: ObjectList) :
        # TODO
        return []


def convert_all_kooc_calls(node_list: list, object_list: ObjectList):
    "Alters the contents of node_list to replace kooc calls with C expressions"

    pass    #TODO
