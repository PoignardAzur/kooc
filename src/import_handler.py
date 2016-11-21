from pyrser.grammar import Grammar

from os.path import realpath
from pathlib import Path
import re

from .object_list import ObjectList


def _get_dir(path: str):
    return "/".join(path.split("/")[:-1])

def get_complete_path(working_file: str, file_path: str):
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

    def __init__(self, silent):
        self._loaded_asts = {}
        self._converted_asts = {}
        self._silent = silent

    def parse_file(self, working_file: str, file_path: str):
        "Parses given file, puts the parsed AST in a cache and returns it"

        from src.kooc_parser import parse_kooc_file

        if not re.search(".*\\.k?h", file_path):
            raise ImportHandlerError(file_path)
        complete_path = get_complete_path(working_file, file_path)
        if (complete_path not in self._loaded_asts):
            silent = self._silent
            ast = parse_kooc_file(self, working_file, file_path, silent, True)
            if not ast:
                raise ImportHandlerError

            self._loaded_asts[complete_path] = ast

        return self._loaded_asts[complete_path]

    def load_objects_in(self, object_list: ObjectList,
                        working_file: str, file_path: str):
        """Applies .get_c_ast(object_list) to all objects in the cached ast

        Returns True if the file hasn't been 'loaded' yet, False otherwise"""

        from src.kooc_parser import convert_ast

        complete_path = get_complete_path(working_file, file_path)
        if (complete_path in self._converted_asts):
            return False
        self._converted_asts[complete_path] = True

        convert_ast(self._loaded_asts[complete_path], object_list)

        return True
