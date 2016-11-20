from cnorm.nodes import *

def wichdecl(decl):
    if type(decl._ctype) is FuncType :
        return "_func"
    else :
        return "_var"

def mangl_pointer(decl):
    if type(decl._decltype) is PointerType:
        return "P" + mangl_pointer(decl._decltype)
    elif type(decl._decltype) is QualType:
        return "" + mangl_pointer(decl._decltype)
    else:
        return ""

def mangl_array(decl):
    return "A" + decl._ctype._expr.value

mangl_tab = {
    "char" : {0 : "char"},
    "int" : {0 : "int", 4 : "long", 5 : "llong", 6 : "short"},
    "float" : {0 : "float"},
    "double" : {0 : "double", 4 : "ldouble"}
}

def mangl_var(decl):
    if type(decl._ctype) is ComposedType :
        return mangl_userDef(decl)
    mangl = "_"
    if type(decl._ctype._decltype) is PointerType:
        mangl += mangl_pointer(decl)
    elif type(decl._ctype._decltype) is ArrayType:
        mangl += mangl_array(decl)
    if hasattr(decl._ctype, "_sign"):
        if decl._ctype._sign == 1 and decl._ctype._identifier == "char":
            mangl += "s"
        if decl._ctype._sign == 2:
            mangl += "u"
    mangl += mangl_tab[decl._ctype._identifier][decl._ctype._specifier]
    return mangl


def mangl_func(decl):
    return mangl_var(decl) + "_" + str(len(decl._ctype._params))

def mangl_userDef(decl):
    if hasattr(decl._ctype, "enums"):
        return "_E" + decl._ctype._identifier
    if decl._ctype._specifier == 1:
        return "_S" + decl._ctype._identifier
    else:
        return "_U" + decl._ctype._identifier

def typeof_decl(decl):
    if type(decl._ctype) is PrimaryType :
        return mangl_var(decl)
    elif type(decl._ctype) is FuncType :
        return mangl_func(decl)
    else :
        return mangl_var(decl)

def mangling(decl, name):
    return "_kooc" + wichdecl(decl) + "_" + name + "_" + decl._name + typeof_decl(decl)
