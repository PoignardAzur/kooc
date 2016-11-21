from src.mangling import mangling

from cnorm.parsing.declaration import Declaration

import unittest

c_parser = Declaration()

def find_decl(decl_list: list, name: str):
    for decl in decl_list:
        if decl._name == name:
            return decl
    return None #ERROR

class TestMangling(unittest.TestCase):

    def test_simple_var(self):

        decl = c_parser.parse("int x;").body[0]
        self.assertEqual(mangling(decl, "Foobar"), "_kooc_var_Foobar_x_int")

    def test_base_types(self):

        decl_list = c_parser.parse("""
            char c;
            signed char Sc;
            unsigned char Uc;
            short s;
            short int si;
            signed short Ss;
            signed short int Ssi;
            unsigned short Us;
            unsigned short int Usi;
            int i;
            signed S;
            signed int Si;
            unsigned U;
            unsigned int Ui;
            long l;
            long int li;
            signed long Sl;
            signed long int Sli;
            unsigned long Ul;
            unsigned long int Uli;
            long long ll;
            long long int lli;
            signed long long Sll;
            signed long long int Slli;
            unsigned long long Ull;
            unsigned long long int Ulli;
            float f;
            double d;
            long double ld;
        """).body

#       TEMPLATE:
#       self.assertEqual(
#           mangling(find_decl(decl_list, "VARNAME"), "Foobar"),
#           "_kooc_var_Foobar_VARNAME_MANGLEDTYPE"
#       )
        self.assertEqual(
            mangling(find_decl(decl_list, "c"), "Foobar"),
            "_kooc_var_Foobar_c_char"
        )
        self.assertEqual(
            mangling(find_decl(decl_list, "Sc"), "Foobar"),
            "_kooc_var_Foobar_Sc_schar"
        )
        self.assertEqual(
            mangling(find_decl(decl_list, "Uc"), "Foobar"),
            "_kooc_var_Foobar_Uc_uchar"
        )
        self.assertEqual(
            mangling(find_decl(decl_list, "s"), "Foobar"),
            "_kooc_var_Foobar_s_short"
        )
        self.assertEqual(
            mangling(find_decl(decl_list, "si"), "Foobar"),
            "_kooc_var_Foobar_si_short"
        )
        self.assertEqual(
            mangling(find_decl(decl_list, "Ss"), "Foobar"),
            "_kooc_var_Foobar_Ss_short"
        )
        self.assertEqual(
            mangling(find_decl(decl_list, "Ssi"), "Foobar"),
            "_kooc_var_Foobar_Ssi_short"
        )
        self.assertEqual(
            mangling(find_decl(decl_list, "Us"), "Foobar"),
            "_kooc_var_Foobar_Us_ushort"
        )
        self.assertEqual(
            mangling(find_decl(decl_list, "Usi"), "Foobar"),
            "_kooc_var_Foobar_Usi_ushort"
        )
        self.assertEqual(
            mangling(find_decl(decl_list, "i"), "Foobar"),
            "_kooc_var_Foobar_i_int"
        )
        self.assertEqual(
            mangling(find_decl(decl_list, "S"), "Foobar"),
            "_kooc_var_Foobar_S_int"
        )
        self.assertEqual(
            mangling(find_decl(decl_list, "Si"), "Foobar"),
            "_kooc_var_Foobar_Si_int"
        )
        self.assertEqual(
            mangling(find_decl(decl_list, "U"), "Foobar"),
            "_kooc_var_Foobar_U_uint"
        )
        self.assertEqual(
            mangling(find_decl(decl_list, "Ui"), "Foobar"),
            "_kooc_var_Foobar_Ui_uint"
        )
        self.assertEqual(
            mangling(find_decl(decl_list, "l"), "Foobar"),
            "_kooc_var_Foobar_l_long"
        )
        self.assertEqual(
            mangling(find_decl(decl_list, "li"), "Foobar"),
            "_kooc_var_Foobar_li_long"
        )
        self.assertEqual(
            mangling(find_decl(decl_list, "Sl"), "Foobar"),
            "_kooc_var_Foobar_Sl_long"
        )
        self.assertEqual(
            mangling(find_decl(decl_list, "Sli"), "Foobar"),
            "_kooc_var_Foobar_Sli_long"
        )
        self.assertEqual(
            mangling(find_decl(decl_list, "Ul"), "Foobar"),
            "_kooc_var_Foobar_Ul_ulong"
        )
        self.assertEqual(
            mangling(find_decl(decl_list, "Uli"), "Foobar"),
            "_kooc_var_Foobar_Uli_ulong"
        )
        self.assertEqual(
            mangling(find_decl(decl_list, "ll"), "Foobar"),
            "_kooc_var_Foobar_ll_llong"
        )
        self.assertEqual(
            mangling(find_decl(decl_list, "lli"), "Foobar"),
            "_kooc_var_Foobar_lli_llong"
        )
        self.assertEqual(
            mangling(find_decl(decl_list, "Sll"), "Foobar"),
            "_kooc_var_Foobar_Sll_llong"
        )
        self.assertEqual(
            mangling(find_decl(decl_list, "Slli"), "Foobar"),
            "_kooc_var_Foobar_Slli_llong"
        )
        self.assertEqual(
            mangling(find_decl(decl_list, "Ull"), "Foobar"),
            "_kooc_var_Foobar_Ull_ullong"
        )
        self.assertEqual(
            mangling(find_decl(decl_list, "Ulli"), "Foobar"),
            "_kooc_var_Foobar_Ulli_ullong"
        )
        self.assertEqual(
            mangling(find_decl(decl_list, "f"), "Foobar"),
            "_kooc_var_Foobar_f_float"
        )
        self.assertEqual(
            mangling(find_decl(decl_list, "d"), "Foobar"),
            "_kooc_var_Foobar_d_double"
        )
        self.assertEqual(
            mangling(find_decl(decl_list, "ld"), "Foobar"),
            "_kooc_var_Foobar_ld_ldouble"
        )

    def test_pointer_types(self):

        pointer_decl_list = c_parser.parse("""
            char *c;
            signed char *Sc;
            unsigned char *Uc;
            char **ppc;
        """).body

        self.assertEqual(
            mangling(find_decl(pointer_decl_list, "c"), "Foobar"),
            "_kooc_var_Foobar_c_Pchar"
        )
        self.assertEqual(
            mangling(find_decl(pointer_decl_list, "Sc"), "Foobar"),
            "_kooc_var_Foobar_Sc_Pschar"
        )
        self.assertEqual(
            mangling(find_decl(pointer_decl_list, "Uc"), "Foobar"),
            "_kooc_var_Foobar_Uc_Puchar"
        )
        self.assertEqual(
            mangling(find_decl(pointer_decl_list, "ppc"), "Foobar"),
            "_kooc_var_Foobar_ppc_PPchar"
        )

    def test_function_types(self):

        function_decl_list = c_parser.parse("""
            char one();
            void two();
            void three(void);
            char four(char c);
            char *five(char *str);
            char *six(void, char *str);
        """).body

        self.assertEqual(
            mangling(find_decl(function_decl_list, "one"), "Foobar"),
            "_kooc_func_Foobar_one_char_0"
        )
        self.assertEqual(
            mangling(find_decl(function_decl_list, "two"), "Foobar"),
            "_kooc_func_Foobar_two_void_0"
        )
        self.assertEqual(
            mangling(find_decl(function_decl_list, "three"), "Foobar"),
            "_kooc_func_Foobar_three_void_0"
        )
        self.assertEqual(
            mangling(find_decl(function_decl_list, "four"), "Foobar"),
            "_kooc_func_Foobar_four_char_1_arg_char"
        )
        self.assertEqual(
            mangling(find_decl(function_decl_list, "five"), "Foobar"),
            "_kooc_func_Foobar_five_Pchar_1_arg_Pchar"
        )
        self.assertEqual(
            mangling(find_decl(function_decl_list, "six"), "Foobar"),
            "_kooc_func_Foobar_six_Pchar_1_arg_Pchar"
        )

    def test_array_types(self):

        array_decl_list = c_parser.parse("""
            char one[10];
            char *two[10];
            char three[10][10];
            char four[];
        """).body

        self.assertEqual(
            mangling(find_decl(array_decl_list, "one"), "Foobar"),
            "_kooc_var_Foobar_one_A10char"
        )
        self.assertEqual(
            mangling(find_decl(array_decl_list, "two"), "Foobar"),
            "_kooc_var_Foobar_two_A10Pchar"
        )
        self.assertEqual(
            mangling(find_decl(array_decl_list, "three"), "Foobar"),
            "_kooc_var_Foobar_three_A10A10char"
        )
        self.assertEqual(
            mangling(find_decl(array_decl_list, "four"), "Foobar"),
            "_kooc_var_Foobar_four_Pchar"
        )

    def test_struct_types(self):

        struct_decl_list = c_parser.parse("""
            struct Test one;
            struct Test *two;
        """).body

        self.assertEqual(
            mangling(find_decl(struct_decl_list, "one"), "Foobar"),
            "_kooc_var_Foobar_one_STest"
        )
        self.assertEqual(
            mangling(find_decl(struct_decl_list, "two"), "Foobar"),
            "_kooc_var_Foobar_two_PSTest"
        )

    def test_enum_types(self):

        enum_decl_list = c_parser.parse("""
            enum Test one;
            enum Test *two;
        """).body

        self.assertEqual(
            mangling(find_decl(enum_decl_list, "one"), "Foobar"),
            "_kooc_var_Foobar_one_ETest"
        )
        self.assertEqual(
            mangling(find_decl(enum_decl_list, "two"), "Foobar"),
            "_kooc_var_Foobar_two_PETest"
        )

    def test_union_types(self):

        union_decl_list = c_parser.parse("""
            union Test one;
            union Test *two;
        """).body

        self.assertEqual(
            mangling(find_decl(union_decl_list, "one"), "Foobar"),
            "_kooc_var_Foobar_one_UTest"
        )
        self.assertEqual(
            mangling(find_decl(union_decl_list, "two"), "Foobar"),
            "_kooc_var_Foobar_two_PUTest"
        )
