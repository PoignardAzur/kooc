#!/usr/bin/env python

from pyrser import meta, grammar
from pyrser.parsing import node
from pyrser.hooks.set import set_node
from cnorm.parsing.declaration import Declaration

import module
import node_implementation

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

    """

@meta.hook(KoocParser)
def add_kooc_decl(self, current_block, ast):
    current_block.ref.body.append(ast.contents)
    return True

@meta.hook(KoocParser)
def create_module(self, ast, contents, module_name):
    ast.contents = module.KoocModule(self.value(module_name), contents.ref.body)
    return True

@meta.hook(KoocParser)
def create_implem(self, ast, contents, module_name):
    ast.contents = node_implementation.KoocImplem(self.value(module_name), contents.ref.body)
    return True

defaultKoocParser = KoocParser()

