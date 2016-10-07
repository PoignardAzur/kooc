#ifndef TEST_H_
# define TEST_H_
# include "Test.h"
#endif

static int f_int(int a)
{
  return (a++);
}

static char f_char(char a)
{
  return (a++);
}

static void f_void(int a, char b)
{
  printf("Test %d %c\n", a, b);
}

struct s_Test Test =
  {
    .a_char = 42,
    .a_double = 3.8,
    .f_int = &f_int,
    .f_char = &f_char,
    .f_void = &f_void
  };
