import sys
from cnorm.parsing.declaration import Declaration
from cnorm.passes import to_c
from cnorm.nodes import *
from pyrser.parsing.node import Node

class KoocModule(Node) :
    def __init__(self, name, fields):
        self.name = name
        self.fields = fields
    def transform(self) :
        tmp_fields = self.fields
        for tmp in tmp_fields:
            tmp._name = self.name + tmp._name
        return fields
