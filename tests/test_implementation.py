from cnorm.nodes import *
from src.at_implementation import AtImplementation
from src.at_module import AtModule

import unittest

par = cnorm.parsing.declaration.Declaration()

AtModule("Empty", [])

implem_empty =
"""
    @implementation Empty
    {
    }
"""

AtModule("Variable", [par.parse("int x;").body[0],
                      par.parse("int y = 3;").body[0],
                      par.parse("float x;").body[0]])

implem_only_variable =
"""
    @implementation Variable
    {
    }
"""

AtModule("Function", [par.parse("int func1(int x);").body[0],
                      par.parse("int func2();").body[0],
                      par.parse("void func1(char a, char b, int *c);").body[0]])

implem_only_function =
"""
    @implementation Function
    {
        int     func1(int x)
        {
            return (-x);
        }

        int     func2()
        {
            return (1);
        }

        void    finc1(char a, char b, int *c)
        {
            *c = a * b;
        }
    }
"""

AtModule("All", [par.parse("int x;").body[0],
                 par.parse("int y = 3;").body[0],
                 par.parse("float x;").body[0],
                 par.parse("int func1(int x);").body[0],
                 par.parse("int func2();").body[0],
                 par.parse("void func1(char a, char b, int *c);").body[0]])

implem_all =
"""
    @implementation All
    {
        int     func1(int x)
        {
            return (-x);
        }

        int     func2()
        {
            return (1);
        }

        void    finc1(char a, char b, int *c)
        {
            *c = a * b;
        }
    }
"""


class TestParseImplement(unittest.TestCase) :
    "Test Parsing for @implementation"

    self.assertEqual(
    KoocParser.parse(implem_empty).body[0],
    AtImplementation("Empty", [])
    )

