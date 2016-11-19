from pyrser.parsing.node import Node
from cnorm.nodes import Raw

from .mangling import mangling
from .at_module import AtModule
from .object_list import ObjectList
from .import_handler import ImportHandler


class KoocImportError(Exception):
    def __init__(self):
        pass


class AtImport(Node):

    def __init__(self, working_file: str, file_path: str, ih: ImportHandler):
        if (working_file == "-"):
            self._working_file = "--UNIT_TEST--"
        else:
            self._working_file = working_file
        self._ih = ih
        self.file_path = file_path
        self.ast = ih.parse_file(working_file, file_path)

    def get_c_ast(self, module_list: ObjectList):
        self._ih.load_objects_in(module_list, self._working_file,self.file_path)

        # Really awful line; TODO - redo this
        lock_name = self.file_path.upper()[:-3].split("/")[-1] + "_H_"

        return [
            Raw("#ifndef " + lock_name + "\n"),
            Raw("# include \"" + self.file_path[:-3] + ".h\"\n"),
            Raw("# define " + lock_name + "\n"),
            Raw("#endif /* !" + lock_name + " */\n"),
        ]
