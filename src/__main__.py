#!/usr/bin/env python3

import sys
from pathlib import Path
from pyrser.error import Diagnostic

from .kooc_parser import KoocParser, parse_kooc_file, convert_ast
from .import_handler import ImportHandler
from .object_list import ObjectList


def convert_filename(filename: str):
    end = filename[-3:]
    if end == ".kh":
        return filename[:-3] + ".h"
    if end == ".kc":
        return filename[:-3] + ".c"
    return filename + ".kc"


def parse_file(filename: str, silent: bool):
    ih = ImportHandler(silent)
    node = parse_kooc_file(ih, "", filename, silent)
    if node is None:
        return False

    object_list = ObjectList()
    c_node = convert_ast(node, object_list)

    file = open(convert_filename(filename), "w")
    file.write(str(c_node.to_c()))
    file.close()
    return True


def main(argv = [], silent = False):
    if len(argv) < 2:
        if not silent:
            print("No input files", file=sys.stderr)
        return False
    for arg in argv[1:]:
        if not parse_file(arg, silent):
            return False
    return True


if __name__ == "__main__":
    main(sys.argv, silent = True)
