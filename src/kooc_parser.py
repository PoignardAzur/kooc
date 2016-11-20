from pyrser import meta, grammar
from cnorm.parsing.declaration import Declaration
from cnorm.passes import to_c

from .import_handler import ImportHandler
from .at_import import AtImport, AtImportParser
from .at_module import AtModule, AtModuleParser
from .at_implementation import AtImplementation, AtImplementationParser
from .kooc_call import KoocCall


class KoocParser(grammar.Grammar,
                AtImportParser,
                AtModuleParser,
                AtImplementationParser
                ):
    "Transforms text in KOOC format to a KOOC AST"

    def __init__(self, import_handler, working_file = "-"):
        grammar.Grammar.__init__(self)
        Declaration.__init__(self)
        self.ih = import_handler
        self.working_file = working_file

    entry = "translation_unit"

    grammar = """
        declaration =
        [
            Declaration.declaration
            | kooc_call
        ]

        kooc_call =
        [
            [
                AtImportParser.at_import
                | AtModuleParser.at_module
                | AtImplementationParser.at_implem
            ]:decl_ast

            #add_kooc_decl(current_block, decl_ast)
        ]
    """

@meta.hook(KoocParser)
def add_kooc_decl(self, current_block, ast):
    current_block.ref.body.append(ast)
    if hasattr(ast, "types"):
        for name, type_ast in ast.types.items():
            current_block.ref.types[name] = type_ast
    return True

defaultKoocParser = KoocParser(ImportHandler())
