from at_module import AtModule

class ObjectList:

    def __init__(self):
        self.list = []

    def add_module(self, module: AtModule):
        self.list.append(module)
