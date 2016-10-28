import sys
from cnorm.parsing.declaration import Declaration
from cnorm.passes import to_c
from cnorm.nodes import *
from pyrser.parsing.node import Node

class KoocModule(Node) :
    def __init__(self, name, fields):
        self.name = name
        self.fields = fields
    def transform() :
        for tmp in fields:
            tmp._name = self.name + tmp_name
        return fields
        
