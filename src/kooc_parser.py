#!/usr/bin/env python

from pyrser import meta, grammar
from pyrser.parsing import node
from pyrser.hooks.set import set_node
from cnorm.parsing.declaration import Declaration

from at_import import AtImport
from at_module import AtModule
from at_implem import AtImplementation
from kooc_call import KoocCall

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

            at_module

            #add_kooc_decl(current_block, decl_ast)
        ]

        at_import =
        [
            "@import" str:filename

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
            Expression.primary_expression
            | kooc_call
        ]

        kooc_call =
        [
            kooc_type?
            '['
            Base.id:module_name
            [
                '.' Base.id:var_name
                | Base.id:func_name [ ':' kooc_type? Expression.expression:expr ]*
            ]
            ']'
        ]

    """

@meta.hook(KoocParser)
def add_kooc_decl(self, current_block, ast):
    current_block.ref.body.append(ast.contents)
    return True

@meta.hook(KoocParser)
def create_import(self, ast, filename):
    ast.contents = AtImport(self.value(module_name).strip('"'))
    return True

@meta.hook(KoocParser)
def create_module(self, ast, contents, module_name):
    ast.contents = AtModule(self.value(module_name), contents.ref.body)
    return True

@meta.hook(KoocParser)
def create_implem(self, ast, contents, module_name):
    ast.contents = AtImplementation(self.value(module_name), contents.ref.body)
    return True

defaultKoocParser = KoocParser()
