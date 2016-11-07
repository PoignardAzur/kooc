from cnorm.nodes import *
from src.at_implementation import AtImplementation
from src.at_module import AtModule

import unittest

AtModule("Empty", [])

implem_empty =
"""
    @implementation Empty
    {
    }
"""

AtModule("Variable", [])

implem_only_variable =
"""
    @implementation Variable
    {
    }
"""

AtModule("Function", )

implem_only_function =
"""
    @implementation Function
    {
        int     f(int x)
        {
            return (-x);
        }
    }
"""
AtModule("All", )

implem_all =
"""
    @implementation All
    {
        int     f(int x)
        {
            return (-x);
        }
    }
"""


class TestImplement(unittest.TestCase) :
