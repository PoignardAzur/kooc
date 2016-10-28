from cnorm.nodes import *

def wichdecl(decl):
    if type(decl._ctype) is PrimaryType :
        return "_var"
    else :
        return "_func"

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
    "double" : {0 : "double"}
}
    
def mangl_var(decl):
    if type(decl._ctype) is ComposedType :
        return mangl_userDef(decl)
    mangl = "_"
    if type(decl._ctype._decltype) is PointerType:
        mangl += mangl_pointer(decl)
    elif type(decl._ctype._decltype) is ArrayType:
        mangl += mangl_array(decl)
    if hasattr(decl, "_sign"):
        if delc._ctype._sign == 1 :
            mangl += "s"
        else:
            mangl += "us"
    mangl += mangl_tab[decl._ctype._identifier][decl._ctype._specifier]
    return mangl
    

def mangl_func(decl):
    return mangl_var(decl)

def mangl_userDef(decl):
    return "_S" + decl._ctype._identifier

def typeof_decl(decl):
    if type(decl._ctype) is PrimaryType :
        return mangl_var(decl)
    elif type(decl._ctype) is FuncType :
        return mangl_func(decl)
    else :
        return mangl_var(decl)

def mangling(decl, name):
    return "_kooc" + wichdecl(decl) + "_" + name + typeof_decl(decl)
    
