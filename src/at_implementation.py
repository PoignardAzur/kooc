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

class AtImplementationParser(grammar.Grammar, Declaration):
    "Creates a KoocModule AST from text"

    entry = "at_implem"

    grammar = """
        at_implem =
        [
            "@implementation" Base.id:module_name
            "{"
                __scope__:current_block
                #new_composed(_, current_block)

                Declaration.declaration*
            "}"

            #create_implem(_,module_name)
        ]
    """

@meta.hook(AtImplementationParser)
def create_implem(self, ast, module_name):
    module_contents = ast.body
    ast.set(AtImplementation(self.value(module_name), module_contents, error.LocationInfo.from_stream(self._stream)))
    return True


class AtImplementation(Node):

    def __init__(self, name: str, fields: list, locinfo: error.LocationInfo):
        self.name = name
        self.fields = fields
        self.locinfo = locinfo

    def convert_node(self, node, module_name):
        node._name = mangling(node, module_name)

    def get_c_ast(self, module_list: ObjectList) :
        module = module_list.find_object(self.name)
        if module is None:
            raise KoocException(self.locinfo, "No corresponding module")
        for field in self.fields:
            if type(field._ctype) is not FuncType:
                print ("Variable declared in @implementation")
                raise KoocException(self.locinfo, "Variable declared in @implementation")
#            else:
 #               if 
        c_fields = copy.deepcopy(self.fields)
        field_names = []
        for field in module.fields:
            if type(field._ctype) is not FuncType:
                c_fields.append(field)
        for field in c_fields:
            self.convert_node(field, self.name)
            field_names.append(field._name)
        return c_fields

# CAMILLE, J'AI FAIT TON BOULOT
# SOIS HEUREUX PUTAIN
