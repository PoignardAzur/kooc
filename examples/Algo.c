#ifndef ALGO_H_
 #include "Algo.h"
 #define ALGO_H_
#endif /* !ALGO_H_ */

int      _KOOC_Algo_IMPLEMENTATION;

int      _kooc_var_Algo_THE_ANSWER_int = 42;
char     _kooc_var_Algo_THE_ANSWER_char = 42;
double   _kooc_var_Algo_THE_ANSWER_double = 4.2;

int         _kooc_func_Algo_max_int_2_arg_int_arg_int(int n1, int n2);
long        _kooc_func_Algo_max_long_2_arg_long_arg_long(long n1, long n2);

int         _kooc_func_Algo_return_the_answer_int_0()
{
    return _kooc_var_Algo_THE_ANSWER_int;
}

int         _kooc_func_Algo_greatest_int_2_arg_Pint_arg_int(int *range, int size)
{
    int     i;
    int     max;

    max = range[0];
    for (i = 1; i < size; ++i)
    {
        max = _kooc_func_Algo_max_int_2_arg_int_arg_int(max, range[i]);
    }
    return max;
}

long        _kooc_func_Algo_greatest_long_2_arg_Pint_arg_int(int *range, int size)
{
    int     i;
    long    max;

    max = range[0];
    for (i = 1; i < size; ++i)
    {
        max = _kooc_func_Algo_max_long_2_arg_long_arg_long(max, range[i]);
    }
    return max;
}

long        _kooc_func_Algo_greatest_long_2_arg_Plong_arg_int(long *range, int size)
{
    int     i;
    long    max;

    max = range[0];
    for (i = 1; i < size; ++i)
    {
        max = _kooc_func_Algo_max_long_2_arg_long_arg_long(max, range[i]);
    }
    return max;
}

int         _kooc_func_Algo_max_int_2_arg_int_arg_int(int n1, int n2)
{
    return (n1 > n2) ? n1 : n2;
}

long        _kooc_func_Algo_max_long_2_arg_long_arg_long(long n1, long n2)
{
    return (n1 > n2) ? n1 : n2;
}
