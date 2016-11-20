from cnorm.nodes import *
from pyrser.parsing.node import Node

from .mangling import mangling
from .object_list import ObjectList

class KoocCallErrorNotExistingModule(Exception):
    pass

class KoocCall(Node):

    def __init__(self, module_name: str, name: str, isFunc = False, args = []):
        #args: List<cnorm.nodes.Expr>
        self.module_name = module_name
        self.name = name
        self.isFunc = isFunc
        self.args = args

    def get_c_ast(self, module_list: ObjectList) :
        # TODO
        print ("LES MODULES ", module_list.list, "\n\n")
        decl = int(0)
        for tmp in module_list.list :
            if tmp.name == self.module_name :
                print("LE MODULE ", tmp.name, "\n\n")
                for tmp_var in tmp.fields :
                    if tmp_var._name.find(self.name) != -1 :
                        decl = tmp_var
                        break
        if type(decl) is int :
            raise KoocCallErrorNotExistingModule
        print ("LA DECLARATION ", decl, "\n\n")
        if type(decl._ctype) is FuncType :
            return Func(Id(mangling(decl, self.module_name)), self.args)
        else:
            return Id(mangling(decl, self.module_name))

    
def handl_composed(object_list : ObjectList, node):
    if type(node) is Func :
        node = handl_func(object_list, node)
    elif type(node) is ArrayType :
        node = handl_Array(object_list, node)
    elif type(node) is Binary :
        node = handl_Binary(object_list, node)
    elif type(node) is KoocCall:
        node = node.get_c_ast(object_list)
    elif type(node) is Decl:
        node = handl_Decl(object_list, node)
    elif type(node) is Expr:
        node = handl_expr(object_list, node)
    elif type(node) is BlockStmt:
        node = handl_blockStmt(object_list, node)
    return node

#Type Func
def handl_func(object_list : ObjectList, node):
    node.expr.call_expr = handl_composed(node.expr.call_expr, object_list)
    for param in node.expr.params :
            param = handl_composed(object_list, param)
    return node                   

#Type ArrayType
def handl_Array(object_list: ObjectList, node):
    node._ctype._decltype._expr = handl_composed(object_list, node._ctype._decltype._expr)
    if hasattr(node, "_assign_expr") :
        node._assign_expr = handl_composed(object_list, node._assign_expr)
    return node

#Type Binary
def handl_Binary(object_list: ObjectList, node):
    if hasattr(node, "call_expr"):
        node.call_expr = handl_composed(object_list, node.call_expr)
    for param in node.params :
        param = handl_composed(object_list, node)
    return node

#Type Decl
def handl_Decl(object_list: ObjectList, node):
    if hasattr(node, "_assign_expr") :
        node._assign_expr = handl_composed(object_list, node._assign_expr)
    node._ctype._decltype = handl_composed(object_list, node._ctype._decltype)
    if hasattr(node, "body") :
        node.body = handl_composed(object_list, node.body)
    return node

#Type Expr
def handl_expr(object_list: ObjectList, node):
    node.expr = handl_composed(object_list, node.expr)
    if hasattr(node, "_assign_expr"):
        node._assign_expr = handl_composed(node._assign_expr)
    return node

#type BlockStmt
def handl_blockStmt(object_list: ObjectList, node) :
    for node_tmp in node.body :
        node_tmp = handl_composed(object_list, node_tmp)
    return node

def iter_all_attr(object_list: ObjectList, node):
    for tmp in dir(node):
        if not tmp.startswith('__'):
            if type(getattr(node, tmp)) is KoocCall:
                setattr(node, tmp, getattr(node, tmp))
        

def convert_all_kooc_calls(node_list: list, object_list: ObjectList):
    for node in node_list :
        print("AVANT ", node, "\n\n")
        node = handl_composed(object_list, node)
        print("APRES", node, "\n\n")
    return node_list
        
