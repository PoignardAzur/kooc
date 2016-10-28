def wichdecl(decl):
    if type(decl._ctype) is PrimaryType :
        return "_var"
    else :
        return "_func"

def typeof_decl(decl):
    
    
def mangling(decl, name):
    return "_kooc" + wichdecl(decl) + "_" + name + typeof_decl(decl)
    
