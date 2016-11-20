class ObjectList:

    def __init__(self):
        self.list = []

    def add_module(self, module):
        self.list.append(module)

    def find_object(self, name: str):
        for obj in self.list:
            if hasattr(obj, "_name") and obj._name == name:
                return obj
            if hasattr(obj, "name") and obj.name == name:
                return obj
        return None
