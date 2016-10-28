#!/usr/bin/env python

import sys
from pathlib import Path
from pyrser.error import Diagnostic
import KoocParser

def convertAST(node):
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
        node = KoocParser.KoocParser().parse_file(filename)
    except Diagnostic as diag:
        sys.stderr.write("Parsing error: " + str(diag) + "\n")
        return

    print(node)

    if True:
        #resolve KOOC calls
        convertAST(node)
        file = open(convert_filename(filename), "w")
        file.write(str(node.to_c()))

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
