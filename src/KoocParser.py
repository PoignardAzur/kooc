#!/usr/bin/env python

from pyrser import meta, grammar
from pyrser.parsing import node
from pyrser.hooks.set import set_node
from pyrser.error import Diagnostic
from cnorm.parsing.declaration import Declaration

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
            __scope__:decl_contents

            at_module

            #add_declaration(current_block, decl_contents)
        ]

        at_module =
        [
            "@module" Base.id:module_name

            "{"
                __scope__:current_block
                #new_composed(_, current_block)

                Declaration.declaration*
            "}"

            #create_module(decl_contents,current_block,module_name)
        ]

    """

@meta.hook(KoocParser)
def add_declaration(self, current_block, ast):
    current_block.ref.body.append(ast)
    return True

@meta.hook(KoocParser)
def create_module(self, ast, contents, module_name):
    ast = {
        "name": self.value(module_name),
        "fields": contents.ref.body
    }
    return True

defaultKoocParser = KoocParser()

