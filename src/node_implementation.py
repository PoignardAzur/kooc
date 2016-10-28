import sys
from pyrser.parsing.node import Node

class KoocImplementation(Node) :
    
    def __init__(self, name, fields):
        self.name = name
        self.fields = fields
        
    def transform() :
        for tmp in fields:
            tmp._name = self.name + tmp_name
        return fields
        
