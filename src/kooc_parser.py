from pyrser import meta, grammar
from cnorm.parsing.declaration import Declaration
from cnorm.nodes import RootBlockStmt
from cnorm.passes import to_c

from pathlib import Path
from subprocess import call

from .import_handler import ImportHandler, get_complete_path
from .at_import import AtImport, AtImportParser
from .at_module import AtModule, AtModuleParser
from .at_implementation import AtImplementation, AtImplementationParser
from .kooc_call import KoocCall, convert_all_kooc_calls
from .object_list import ObjectList


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
            |
            [
                [
                    AtImportParser.at_import
                    | AtModuleParser.at_module
                    | AtImplementationParser.at_implem
                ]:decl_ast

                #add_kooc_decl(current_block, decl_ast)
            ]
        ]

        primary_expression =
        [
            // Creates weird errors; should examine Expression source before
            // uncommenting
            Declaration.primary_expression:>_
            | kooc_call:>_
        ]

       kooc_call =
        [
            [kooc_type:type #set_type(_, type)]?
            "["
            Base.id:module_name
            [
                ["." Base.id:var_name #create_call_var(_, module_name, var_name)]
                |
                [ Base.id:func_name #create_call_func(_, module_name, func_name)
                [ ":" kooc_type? Expression.expression:expr #create_call_func_addExpr(_, expr)]*
                #create_call_func_push(_)]
            ]
            "]"
        ]

        kooc_type =
        [
            "@!(" Base.id ")"
        ]
    """

@meta.hook(KoocParser)
def add_kooc_decl(self, current_block, ast):
    current_block.ref.body.append(ast)
    if hasattr(ast, "types"):
        for name, type_ast in ast.types.items():
            current_block.ref.types[name] = type_ast
    return True


@meta.hook(KoocParser)
def set_type(self, ast, typee):
    ast.typee = self.value(typee)[3:]
    ast.typee = ast.typee[:-1]
    return True

@meta.hook(KoocParser)
def create_call_var(self, ast, module_name, var_name):
    typeExpr = ""
    if hasattr(ast, "typee"):
        typeExpr = ast.typee
    ast.set(KoocCall(self.value(module_name), self.value(var_name), typeExpr, False, None))
    return True

@meta.hook(KoocParser)
def create_call_func(self, ast, module_name, func_name):
    ast.typeExpr = ""
    if hasattr(ast, "typee"):
        ast.typeExpr = ast.typee
    ast.module = self.value(module_name)
    ast.func = self.value(func_name)
    ast.expr = []
    return True

@meta.hook(KoocParser)
def create_call_func_addExpr(self, ast, Expr):
    ast.expr.append(self.value(Expr))
    return True

@meta.hook(KoocParser)
def create_call_func_push(self, ast) :
    ast.set(KoocCall(ast.module, ast.func, ast.typeExpr, True, ast.expr))
    return True


def parse_kooc_file(import_handler, working_file: str, filename: str,
                    silent: bool, imported = False):
    if (not silent) and (not imported):
        print("Parsing file " + filename)
    complete_path = get_complete_path(working_file, filename)
    if not Path(complete_path).is_file():
        if not silent:
            msg = "Error: " + str(arg) + " does not exist or isn't a file"
            print(msg, file=sys.stderr)
        return None
    try:
        #path_begin = ".".join(complete_path.split(".")[:-1])
        #call(["cpp", complete_path, path_begin + ".kpp"])

        node = KoocParser(import_handler, working_file).parse_file(filename)
        return node
    except Diagnostic as diag:
        if not silent:
            sys.stderr.write("Parsing error: " + str(diag) + "\n")
        if imported:
            raise Diagnostic()
        return None


def convert_node(node, object_list: ObjectList):
    if hasattr(node, "get_c_ast"):
        return node.get_c_ast(object_list)
    else:
        return [node]

def convert_ast(ast, object_list: ObjectList):
    decl_list = []

    try:
        for decl in ast.body:
            decl_list.extend(convert_node(decl, object_list))
        convert_all_kooc_calls(decl_list, object_list)
    except KoocException as exc:
        print(exc.get_error_message())
    return RootBlockStmt(decl_list)
