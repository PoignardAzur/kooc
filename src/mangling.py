from cnorm.nodes import *

def wichdecl(decl):
    if type(decl._ctype) is FuncType :
        return "_func"
    else :
        return "_var"

def resolveDeclType(decl):
    resolvedDeclType = "_"
    dType = decl._ctype

    while hasattr(dType, "_decltype") and dType._decltype:
        if type(dType._decltype) == ArrayType:
            if hasattr(dType._decltype._expr, "value"):
                resolvedDeclType += "A"
                resolvedDeclType += dType._decltype._expr.value
            else:
                resolvedDeclType += "P"
        elif type(dType._decltype) == PointerType:
            resolvedDeclType += "P"
        dType = dType._decltype

    return resolvedDeclType

mangl_tab = {
    "char" : {0 : "char"},
    "int" : {0 : "int", 4 : "long", 5 : "llong", 6 : "short"},
    "float" : {0 : "float"},
    "double" : {0 : "double", 4 : "ldouble"},
    "void" : {0 : "void"}
}

def mangl_var(decl):
    mangl = resolveDeclType(decl)
    if type(decl._ctype) is ComposedType :
        return mangl + mangl_userDef(decl)
    if hasattr(decl._ctype, "_sign"):
        if decl._ctype._sign == 1 and decl._ctype._identifier == "char":
            mangl += "s"
        if decl._ctype._sign == 2:
            mangl += "u"
    mangl += mangl_tab[decl._ctype._identifier][decl._ctype._specifier]
    return mangl


def mangl_func(decl):
    params = []
    for p in decl._ctype._params:
        if typeof_decl(p) != "_void":
            params.append(p)
    nbParams = len(params)
    args = ""
    if nbParams > 0:
        args = "_arg" + "".join([typeof_decl(d) for d in params])
    return mangl_var(decl) + "_" + str(nbParams) + args

def mangl_userDef(decl):
    if decl._ctype._specifier == 1:
        return "S" + decl._ctype._identifier
    elif decl._ctype._specifier == 2:
        return "U" + decl._ctype._identifier
    elif decl._ctype._specifier == 3:
        return "E" + decl._ctype._identifier

def typeof_decl(decl):
    if type(decl._ctype) is FuncType :
        return mangl_func(decl)
    else :
        return mangl_var(decl)

def mangling(decl, name):
    return "_kooc" + wichdecl(decl) + "_" + name + "_" + decl._name + typeof_decl(decl)
