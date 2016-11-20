from pyrser import meta, grammar
from pyrser.parsing import node
from pyrser.hooks.set import set_node
from cnorm.parsing.declaration import Declaration
from cnorm.passes import to_c

from .at_import import AtImport
from .at_module import AtModule
from .at_implementation import AtImplementation
from .kooc_call import KoocCall

class KoocParser(grammar.Grammar, Declaration):
    """Transforms text in KOOC format to a KOOC AST"""

    entry = "translation_unit"

    grammar = """
        declaration =
        [
            Declaration.declaration
            | kooc_declaration
        ]

        kooc_declaration =
        [
            __scope__:decl_ast

            [
                at_import
                | at_module
                | at_implem
            ]

            #add_kooc_decl(current_block, decl_ast)
        ]

        at_import =
        [
            "@import" string:filename

            #create_import(decl_ast,filename)
        ]

        at_module =
        [
            "@module" Base.id:module_name

            "{"
                __scope__:current_block
                #new_composed(_, current_block)

                Declaration.declaration*
            "}"

            #create_module(decl_ast,current_block,module_name)
        ]

        at_implem =
        [
            "@implementation" Base.id:module_name

            "{"
                __scope__:current_block
                #new_composed(_, current_block)

                Declaration.declaration*
            "}"

            #create_implem(decl_ast,current_block,module_name)
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
            [kooc_type]*
            "["
            Base.id:module_name
            [
                ["." Base.id:var_name #create_call_var(_, module_name, var_name)]
                | [Base.id:func_name #create_call_func(_, module_name, func_name)
                   [ ':' [kooc_type]* Expression.expression:expr #create_call_func_addExpr(_, expr)]*
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
    current_block.ref.body.append(ast.contents)
    if hasattr(ast, "types"):
        for name, type_ast in ast.types.items():
            current_block.ref.types[name] = type_ast
    return True

@meta.hook(KoocParser)
def create_import(self, ast, filename):
    ast.contents = AtImport(self.value(filename).strip('"'), KoocParser())
    ast.types = ast.contents.ast.types
    return True

@meta.hook(KoocParser)
def create_module(self, ast, contents, module_name):
    ast.contents = AtModule(self.value(module_name), contents.ref.body)
    return True

@meta.hook(KoocParser)
def create_implem(self, ast, contents, module_name):
    ast.contents = AtImplementation(self.value(module_name), contents.ref.body)
    return True

@meta.hook(KoocParser)
def create_call_var(self, ast, module_name, var_name):
    ast.set(KoocCall(self.value(module_name), self.value(var_name), False, None))
    return True

@meta.hook(KoocParser)
def create_call_func(self, ast, module_name, func_name):
    ast.typeExpr = self.value(typeExpr)
    ast.module = self.value(module_name)
    ast.func = self.value(func_name)
    ast.expr = []

@meta.hook(KoocParser)
def create_call_func_addExpr(self, ast, Expr):
    ast.expr.append(self.value(Expr))

@meta.hook(KoocParser)
def create_call_func_push(self, ast) :
    ast.set(KoocCall(ast.module_name, ast.func, True, ast.expr))
    return True
 
defaultKoocParser = KoocParser()
