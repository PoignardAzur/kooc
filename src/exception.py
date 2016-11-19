from cnorm.parsing.declaration import Declaration
from cnorm.passes import to_c

try:
    cparse = Declaration()
    ast = cparse.parse_file("test.c")
    print(ast.to_c())
except:
    print("Error catched")
