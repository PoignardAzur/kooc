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

void    _kooc_Stackint_int_init_m_Stackint_ptr_int(struct Stackint *self, int size)
{
  int     *buf;
  self->_kooc_nbitem = 0;
  self->_kooc_size = size;
  buf = (int *) calloc(size, sizeof(int));
  self->_kooc_data = buf;
}

int     _kooc_Stackint_int_nbitem_m_Stackint_ptr(struct Stackint *self)
{
  int n;
  n = self->_kooc_nbitem;
  return (n);
}

int     _kooc_Stackint_int_push_m_Stackint_ptr_int(struct Stackint *self, int i)
{
  int pos;
  int *buf;

  pos = self->_kooc_nbitem;
  buf = self->_kooc_data;
  buf[pos++] = i;
  self->_kooc_nbitem = pos;
}
