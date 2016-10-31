#!/usr/bin/env python3

import sys
from pathlib import Path
from pyrser.error import Diagnostic

from koocParser import KoocParser
from convert_kooc_calls import convert_kooc_calls


def convert_ast(node):
    decl_list = []
    for decl in node.body:
        if hasattr(decl, "transform"):
            decl_list.extend(decl.transform())
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
    if not Path(filename).is_file():
        sys.stderr.write("Error: " + str(filename) + " does not exist or isn't a file\n")
        return
    print("Parsing file " + filename)
    try:
        node = KoocParser().parse_file(filename)
        convert_ast(node)
        convert_kooc_calls(node)
        file = open(convert_filename(filename), "w")
        file.write(str(node.to_c()))
    except Diagnostic as diag:
        sys.stderr.write("Parsing error: " + str(diag) + "\n")
        return


def main(argv):
    if len(argv) < 2:
        sys.exit("No input files")
    for arg in argv[1:]:
        try:
            parse_file(arg)
        except Exception as e:
            sys.exit("An exception of type " + str(type(e)) + " was raised: " + str(e.args))
        except:
            sys.exit("An unknown exception was raised")


if __name__ == "__main__":
    main(sys.argv)
