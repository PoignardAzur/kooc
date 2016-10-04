#ifndef TEST_H_
# define TEST_H_
# include "Test.h"
#endif  

int	main(int ac, char **av)
{
  Test.a_int = 10;
  Test.a_char = Test.f_char(Test.a_char);
  Test.f_void(Test.a_int, Test.a_char);

  return (Test.f_int(Test.a_int));
}
