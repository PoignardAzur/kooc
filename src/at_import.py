from pyrser import meta, grammar
from pyrser.parsing.node import Node
from cnorm.parsing.declaration import Declaration
from cnorm.nodes import Raw

from .mangling import mangling
from .at_module import AtModule
from .object_list import ObjectList
from .import_handler import ImportHandler


class AtImportParser(grammar.Grammar, Declaration):
    "Creates a AtImport AST from text"

    def __init__(self, import_handler, working_file = "-"):
        grammar.Grammar.__init__(self)
        Declaration.__init__(self)
        self.ih = import_handler
        self.working_file = working_file

    entry = "at_import"

    grammar = """
        at_import =
        [
            "@import" string:filename

            #create_import(_,filename)
        ]
    """

@meta.hook(AtImportParser)
def create_import(self, ast, filename):
    decl = AtImport(
        self.working_file,
        self.value(filename).strip('"'),
        self.ih
    )
    ast.set(decl)
    ast.types = decl.ast.types
    return True


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
