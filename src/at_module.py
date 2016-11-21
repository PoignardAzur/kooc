import copy

from pyrser import meta, grammar
from pyrser.parsing.node import Node
from pyrser import error
from cnorm.nodes import FuncType
from cnorm.nodes import Storages, Qualifiers, Specifiers, Signs
from cnorm.parsing.declaration import Declaration

from .mangling import mangling
from .object_list import ObjectList
from .exception import KoocException

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
    ast.set(AtModule(self.value(module_name), module_contents, error.LocationInfo.from_stream(self._stream)))
    return True


class AtModule(Node):

    def __init__(self, name: str, fields: list, locinfo: error.LocationInfo):
        self.name = name
        self.fields = fields
        self.locinfo = locinfo

    def convert_node(self, node, module_name):
        storage = node._ctype._storage
        if storage == Storages.TYPEDEF:
            raise KoocException(self.locinfo, "An error occured")
        if storage == Storages.STATIC:
            raise KoocException(self.locinfo, "An error occured")
        if storage == Storages.EXTERN:
            raise KoocException(self.locinfo, "An error occured")
        if hasattr(node, "body") and storage != Storages.INLINE:
            raise KoocException(self.locinfo, "An error occured")
        if hasattr(node, "body"):
            node._ctype._storage = Storages.STATIC
        elif type(node._ctype) is not FuncType:
            node._ctype._storage = Storages.EXTERN
        node._name = mangling(node, module_name)

    def get_c_ast(self, module_list: ObjectList):

        if module_list.find_object(self.name):
            raise KoocException(self.locinfo, "Modules and/or variables cannot share the same name")
        module_list.add_module(self)

        c_fields = copy.deepcopy(self.fields)
        field_names = []
        for field in c_fields:
            self.convert_node(field, self.name)
            if field._name in field_names:
                raise KoocException(self.locinfo, "Variable/function duplicate")
            field_names.append(field._name)
        return c_fields
