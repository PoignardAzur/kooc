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

AtModule("Variable", [par.parse("int x;"),
                      par.parse("int y = 3;"),
                      par.parse("float x;")])

implem_only_variable =
"""
    @implementation Variable
    {
    }
"""

AtModule("Function", [par.parse("int func1(int x);"),
                      par.parse("int func2();"),
                      par.parse("void func1(char a, char b, int *c);")])

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
AtModule("All", [par.parse("int x;"),
                 par.parse("int y = 3;"),
                 par.parse("float x;"),
                 par.parse("int func1(int x);"),
                 par.parse("int func2();"),
                 par.parse("void func1(char a, char b, int *c);")])

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


class TestImplement(unittest.TestCase) :
