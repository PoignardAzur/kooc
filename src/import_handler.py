from pyrser.grammar import Grammar

from os.path import realpath
from pathlib import Path
import re

from .object_list import ObjectList


def _get_dir(path: str):
    return "/".join(path.split("/")[:-1])

def _get_complete_path(working_file: str, file_path: str):
    "Resolves relative paths"

    if working_file == "" or working_file == "-":
        return realpath(file_path)
    else:
        return realpath(_get_dir(working_file) + "/" + file_path)


class ImportHandlerError(Exception):
    def __init__(self, str = ""):
        self.str = str
    def __str__(self):
        return self.str


class ImportHandler:

    def __init__(self):
        self._loaded_asts = {}
        self._converted_asts = {}

    def parse_file(self, working_file: str, file_path: str):
        "Parses given file, puts the parsed AST in a cache and returns it"

        from src.kooc_parser import KoocParser

        if not re.search(".*\\.k?h", file_path):
            raise ImportHandlerError(file_path)
        complete_path = _get_complete_path(working_file, file_path)
        if not Path(complete_path).is_file():
            raise ImportHandlerError("CAN'T FIND " + complete_path)
        if (complete_path not in self._loaded_asts):
            kooc_parser = KoocParser(self, _get_dir(complete_path))
            ast = kooc_parser.parse_file(complete_path)
            self._loaded_asts[complete_path] = ast
        #TODO replace with standardized parsing

        return self._loaded_asts[complete_path]

    def load_objects_in(self, object_list: ObjectList,
                        working_file: str, file_path: str):
        """Applies .get_c_ast(object_list) to all objects in the cached ast

        Returns True if the file hasn't been 'loaded' yet, False otherwise"""

        complete_path = _get_complete_path(working_file, file_path)
        if (complete_path in self._converted_asts):
            return False
        self._converted_asts[complete_path] = True

        for decl in self._loaded_asts[complete_path].body:
            if hasattr(decl, "get_c_ast"):
                decl.get_c_ast(object_list)
        #TODO replace with standardized conversion

        return True
