import copy

from pyrser import meta, grammar
from pyrser.parsing.node import Node
from cnorm.nodes import FuncType
from cnorm.parsing.declaration import Declaration

from .mangling import mangling
from .object_list import ObjectList


class AtModuleParser(grammar.Grammar, Declaration):
    "Creates a AtModule AST from text"

    entry = "at_module"

    grammar = """
        at_module =
        [
            "@module" Base.id:module_name
            "{"
                __scope__:current_block
                #new_composed(_, current_block)

                Declaration.declaration*
            "}"

            #create_module(_,module_name)
        ]
    """

@meta.hook(AtModuleParser)
def create_module(self, ast, module_name):
    module_contents = ast.body
    ast.set(AtModule(self.value(module_name), module_contents))
    return True


class AtModuleErrorMultiModule(Exception):
    pass

class AtModuleErrorMultiObj(Exception):
    pass

class AtModuleErrorNotInlineFonction(Exception):
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
            if type(field._ctype) is FuncType and hasattr(field, "body") and field._ctype._storage != 5:
                raise AtModuleErrorNotInlineFonction
            field._name = mangling(field, field._name)
            if field._name in check:
                raise AtModuleErrorMultiObj
            check.append(field._name)
        return c_fields
