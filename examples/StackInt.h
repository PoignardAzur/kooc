#ifndef STACKINT_H_
#define STACKINT_H_

#ifndef ALGO_H_
 #include "Algo.h"
 #define ALGO_H_
#endif /* !ALGO_H_ */

typedef struct StackInt StackInt;
struct StackInt
{
    char    _kooc_var__foobar_char;
    char    _kooc_var__foobar_int;

    int	    _kooc_var__size_int;
    int	    *_kooc_var__data_int_ptr;
};

void    _kooc_func_Stackint__foobar_void_Stackint_ptr(StackInt *self);

int     _kooc_func_StackInt_getSize_int_StackInt_ptr(StackInt *self);
void    _kooc_func_StackInt_init_void_StackInt_ptr_int(StackInt *self, int stackSize);
void    _kooc_func_StackInt_clean_void_StackInt_ptr(StackInt *self);
void    _kooc_func_StackInt_push_void_StackInt_ptr_int(StackInt *self, int newVal);
int     _kooc_func_StackInt_pop_int_StackInt_ptr(StackInt *self);
int     _kooc_func_StackInt_getMax_int_StackInt_ptr(StackInt *self);

StackInt    *_kooc_func_StackInt_alloc_StackInt_ptr_void();
StackInt    *_kooc_func_StackInt_new_StackInt_ptr_int(int stackSize);
void        _kooc_func_StackInt_delete_void_StackInt_ptr(StackInt *self);

extern int _kooc_var_Stackint_nbStack_int;

#endif /* STACKINT_H_ */
