#ifndef ALGO_H_
 #include "Algo.h"
 #define ALGO_H_
#endif /* !ALGO_H_ */

int      _kooc_Algo_int_THE_ANSWER = 42;
char     _kooc_Algo_char_THE_ANSWER = 42;
double   _kooc_Algo_double_THE_ANSWER = 4.2;

int         _kooc_Algo_max_int_int_int(int n1, int n2);
long        _kooc_Algo_max_long_long_long(long n1, long n2);

int         _kooc_Algo_return_the_answer_int_void()
{
    return @!(int)[Algo.THE_ANSWER];
}

int         _kooc_Algo_greatest_int_int_int(int *range, int size)
{
    int     i;
    int     max;

    max = size[0];
    for (i = 1; i < size; ++i)
    {
        max = _kooc_Algo_max_int_int_int(max, size[i]);
    }
    return max;
}

long        _kooc_Algo_greatest_long_int_int(int *range, int size)
{
    int     i;
    long    max;

    max = size[0];
    for (i = 1; i < size; ++i)
    {
        max = _kooc_Algo_max_long_long_long(max, size[i]);
    }
    return max;
}

long        _kooc_Algo_greatest_long_long_int(long *range, int size)
{
    int     i;
    long    max;

    max = size[0];
    for (i = 1; i < size; ++i)
    {
        max = _kooc_Algo_max_long_long_long(max, size[i]);
    }
    return max;
}

int         _kooc_Algo_max_int_int_int(int n1, int n2)
{
    return (n1 > n2) ? n1 : n2;
}

long        _kooc_Algo_max_long_long_long(long n1, long n2)
{
    return (n1 > n2) ? n1 : n2;
}
