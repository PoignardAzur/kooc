from pyrser.parsing.node import Node
from pyrser.grammar import Grammar

from pathlib import Path
import re

from cnorm.nodes import Raw

from .mangling import mangling
from .at_module import AtModule
from .object_list import ObjectList

class KoocImportError(Exception):
    def __init__(self):
        pass

class AtImport(Node):

    def __init__(self, filename: str, kooc_parser: Grammar):

        if not re.search(".*\\.kh", filename):
            raise KoocImportError()
        if not Path(filename).is_file():
            raise KoocImportError()
        self.filename = filename
        self.ast = kooc_parser.parse_file(filename)

    def get_c_ast(self, module_list: ObjectList) :
        for node in self.ast.body:
            if type(node) == AtModule:
                module_list.add_module(node)

        # Really awful line; TODO - redo this
        lock_name = self.filename.upper()[:-3].split("/")[-1] + "_H_"

        return [
            Raw("#ifndef " + lock_name + "\n"),
            Raw("# include \"" + self.filename[:-3] + ".h\"\n"),
            Raw("# define " + lock_name + "\n"),
            Raw("#endif /* !" + lock_name + " */\n"),
        ]
