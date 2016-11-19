from pyrser.parsing.node import Node

class AtClass(Node):
    """At class instruction implementation"""
    def __init__(self, name: str, fields: list):
        self.name = name
        self.fields = fields
