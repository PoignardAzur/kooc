import copy

from pyrser import meta, grammar
from pyrser.parsing.node import Node
from cnorm.nodes import FuncType
from cnorm.nodes import Storages, Qualifiers, Specifiers, Signs
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


class AtModuleError(Exception):
    pass

class AtModule(Node):

    def __init__(self, name: str, fields: list):
        self.name = name
        self.fields = fields

    def convert_node(self, node, module_name):
        storage = node._ctype._storage
        if storage == Storages.TYPEDEF:
            raise AtModuleError
        if storage == Storages.STATIC:
            raise AtModuleError
        if storage == Storages.EXTERN:
            raise AtModuleError
        if hasattr(node, "body") and storage != Storages.INLINE:
            raise AtModuleError
        if hasattr(node, "body"):
            node._ctype._storage = Storages.STATIC
        elif type(node._ctype) is not FuncType:
            node._ctype._storage = Storages.EXTERN
        node._name = mangling(node, module_name)

    def get_c_ast(self, module_list: ObjectList):

        if module_list.find_object(self.name):
            raise AtModuleError()
        module_list.add_module(self)

        c_fields = copy.deepcopy(self.fields)
        field_names = []
        for field in c_fields:
            self.convert_node(field, self.name)
            if field._name in field_names:
                raise AtModuleError
            field_names.append(field._name)
        return c_fields
