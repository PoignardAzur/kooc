#ifndef TEST_H_
# define TEST_H_

extern int _kooc_Test_int_a;
extern char _kooc_Test_char_a;
extern double _kooc_Test_double_a;

int _kooc_Test_int_f_int(int);
char _kooc_Test_char_f_char(char);
void _kooc_Test_void_f_int_char(int, char);
int _kooc_Test_int_foobar();

typedef struct StackInt StackInt;
struct StackInt
{
  int	_kooc_size;
  int	_kooc_nbitem;
  int	*_kooc_data;
};

void	_kooc_Stackint_int_init_m_Stackint_ptr_int(struct Stackint *, int);
void    _kooc_Stackint_int_clean_m_Stackint_ptr_int(struct Stackint *, int);
int	_kooc_Stackint_int_nbitem_m_Stackint_ptr(struct Stackint *);
int	_kooc_Stackint_int_push_m_Stackint_ptr_int(struct Stackint *, int);
int	_kooc_Stackint_int_f_Stackint_ptr(struct Stackint *);


extern int _kooc_Stackint_int_nbStack;

#endif /* TEST_H_ */
