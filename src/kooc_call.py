from cnorm.nodes import *
from pyrser.parsing.node import Node

from .mangling import mangling
from .object_list import ObjectList

class KoocCallErrorNotExistingModule(Exception):
    pass

class KoocCall(Node):

    def __init__(self, module_name: str, name: str, isFunc = False, args = []):
        #args: List<cnorm.nodes.Expr>
        self.module_name = module_name
        self.name = name
        self.isFunc = isFunc
        self.args = args

    def get_c_ast(self, module_list: ObjectList) :
        # TODO
        decl = int(0)
        for tmp in module_list.list :
            if tmp.name == self.module_name :
                for tmp_var in tmp.fields :
                    if tmp_var._name.find(self.name) != -1 :
                        decl = tmp_var
                        break
        if type(decl) is int :
            raise KoocCallErrorNotExistingModule
        if type(decl._ctype) is FuncType :
            return Func(Id(decl._name), self.args)
        else:
            return Id(decl._name)


def convert_all_kooc_calls(node_list: list, object_list: ObjectList):
    "Alters the contents of node_list to replace kooc calls with C expressions"

    pass    #TODO
