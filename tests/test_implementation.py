from cnorm.nodes import *
from src.at_implementation import AtImplementation
from src.at_module import AtModule

import unittest

par = cnorm.parsing.declaration.Declaration()

implem_empty =
"""
    @implementation Empty
    {
    }
"""

MVariable = AtModule("Variable", [par.parse("int x;").body[0],
                      par.parse("int y = 3;").body[0],
                      par.parse("float x;").body[0]])

implem_only_variable =
"""
    @implementation Variable
    {
    }
"""

MFunction = AtModule("Function", [par.parse("int func1(int x);").body[0],
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

MAll = AtModule("All", [par.parse("int x;").body[0],
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

        void    func1(char a, char b, int *c)
        {
            *c = a * b;
        }
    }
"""

par = cnorm.parsing.declaration.Declaration()
kooc_parser = kooc_parser.KoocParser()
class TestParseImplement(unittest.TestCase) :
    "Test Parsing for @implementation"

    self.assertEqual(
    kooc_parser.parse(implem_empty).body[0],
    AtImplementation("Empty", par.parse("{}"))
    )

    self.assertEqual(
    kooc_parser.parse(implem_only_variable).body[0],
    AtImplementation("Variable", par.parse("{}"))
    )

    self.assertEqual(
    kooc_parser.parse(implem_only_function).body[0],
    AtImplementation("Function", par.parse("""
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
    """))
    )

    self.assertEqual(
    kooc_parser.parse(implem_all).body[0],
    AtImplementation("All", par.parse("""
    {
        int     func1(int x)
        {
            return (-x);
        }

        int     func2()
        {
            return (1);
        }

        void    func1(char a, char b, int *c)
        {
            *c = a * b;
        }
    }
    """))
    )

class TestGetCAstImplemet(unittest.TestCase) :
    "Test get_c_ast for @implementation"

    self.assertEqual(0, 0)
