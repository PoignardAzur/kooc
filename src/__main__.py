#!/usr/bin/env python3

import sys
from pathlib import Path
from pyrser.error import Diagnostic

from .kooc_parser import KoocParser
from .kooc_call import convert_all_kooc_calls
from .object_list import ObjectList


def convert_ast(node, object_list: ObjectList):
    decl_list = []
    for decl in node.body:
        if hasattr(decl, "get_c_ast"):
            decl_list.extend(decl.get_c_ast(object_list))
        else:
            decl_list.append(decl)
    node.body = decl_list


def convert_filename(filename: str):
    end = filename[-3:]
    if end == ".kh":
        return filename[:-3] + ".h"
    if end == ".kc":
        return filename[:-3] + ".c"
    return filename + ".kc"


def parse_file(filename: str):
    print("Parsing file " + filename)
    try:
        node = KoocParser().parse_file(filename)
        object_list = ObjectList()
        convert_ast(node, object_list)
        convert_all_kooc_calls(node.body, object_list)
        file = open(convert_filename(filename), "w")
        # file.write(str(node.to_c()))
        file.close()
    except Diagnostic as diag:
        sys.stderr.write("Parsing error: " + str(diag) + "\n")
        return False
    return True


def main(argv = []):
    if len(argv) < 2:
        sys.stderr.write("No input files\n")
        return False
    for arg in argv[1:]:
        if not Path(arg).is_file():
            sys.stderr.write("Error: " + str(arg) +
                " does not exist or isn't a file\n")
            return False
        elif not parse_file(arg):
            return False
    return True


if __name__ == "__main__":
    main(sys.argv)
