# include "Test.h"

int	main(int ac, char **av)
{
  _kooc_Test_int_a = 10;
  _kooc_Test_char_a = _kooc_Test_char_f_char(_kooc_Test_char_a);
  _kooc_Test_void_f_int_char(_kooc_Test_int_a, _kooc_Test_char_a);

  struct Stackint        t;
  struct Stackint        *tp;
  void            *t2;

  _kooc_Stackint_int_init_m_Stackint_ptr_int(&t);
  return  _kooc_Test_int_f_int(_kooc_Test_int_a);
}
