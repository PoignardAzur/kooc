# include "Test.h"

int _kooc_Test_int_a;
char _kooc_Test_char_a = 42;
double _kooc_Test_double_a = 3.8;
static _kooc_Test_int_b = 89;

int _kooc_Test_int_f_int(int a)
{
  return (a++);
}

char _kooc_Test_char_f_char(char a)
{
  return (a++);
}

void _kooc_Test_void_f_int_char(int a, char b)
{
  printf("Test %d %c\n", a, b);
}

int _kooc_Test_int_foobar()
{
  return 0;
}
