import copy

from pyrser import meta, grammar
from pyrser.parsing.node import Node
from cnorm.parsing.declaration import Declaration

from .mangling import mangling
from .object_list import ObjectList


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
    ast.set(AtImplementation(self.value(module_name), module_contents))
    return True


class AtImplementation(Node):

    def __init__(self, name: str, fields: list):
        self.name = name
        self.fields = fields

    def get_c_ast(self, module_list: ObjectList) :
        # TODO
        return []
