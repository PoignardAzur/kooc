import sys
from cnorm.parsing.declaration import Declaration
from cnorm.passes import to_c
from cnorm.nodes import *

class KoocModule(Node) :
    def __init__(self, name, fields):
        self.name = name
        self.fields = fields
    def transform() :
        return 0
        
