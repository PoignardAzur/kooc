import sys
from cnorm.parsing.declaration import Declaration
from cnorm.passes import to_c
from pyrser import error

class Position():
      def __init__(self, path: str, line: int, col: int):
            
            self.path = path
            self.line = line
            self.col = col

class ErrorClass():
      def __init__(self, pos: Position):

            self.msg = msg
            self.pos = pos

      def get_error_message(self):
            new_msg = "In file " + self.pos.path + " at line " + self.pos.line + " and column " + self.pos.col + ": \n" + self.msg
            return new_msg

      def output_Warning(self):
             print(self.get_error_message(), file=sys.stderr)

def my_get_content(self) -> str:
    f = open(self.filepath, 'r')
    lines = list(f)
    f.close()
    if self.line - 1 >= len(lines):
        txtline = lines[self.line - 2]
    else:
        txtline = lines[self.line - 1]
    if txtline[-1] != '\n':
        txtline += '\n'
    indent = ' ' * (self.col - 1)
    if self.size != 1:
        indent += '~' * (self.size)
    else:
        indent += '^'
    txt = "from {f} at line:{l} col:{c} :\n{content}{i}".format(
        f=self.filepath,
        content=txtline,
        l=self.line,
        c=self.col,
        i=indent
    )
    return txt
