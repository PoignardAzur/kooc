from cnorm.parsing.declaration import Declaration
from cnorm.passes import to_c
from pyrser import error

class ErrorClass():
      def __init__(self, msg: str = None, filepath: str = None, col: str = None, line: str = None, diagnostic: error.Notification = None):
            if diagnostic is not None:
                  self.msg = diagnostic.get_content(True, True)
                  self.filepath = diagnostic.location.filepath
                  self.col = diagnostic.location.col
                  self.line = diagnostic.location.line
                  self.diagnostic = True
            else :
                  self.msg = msg
                  self.filepath = details
                  self.col = col
                  self.line = line
                  self.diagnostic = False

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

error.LocationInfo.get_content = my_get_content
try:
    cparse = Declaration()
    ast = cparse.parse_file("test.c")
    print(ast.to_c())
except error.Diagnostic as e:
    print(e)
    print(e.logs[0].get_content(True, True))
