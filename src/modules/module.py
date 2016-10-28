import sys
from cnorm.parsing.declaration import Declaration
from cnorm.passes import to_c
from cnorm.nodes import *

class KoocModule(Declaration) :
    def __init__(self, name, field):
        self.name = name
        self.field = field
    
