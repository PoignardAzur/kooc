#ifndef STACKINT_H_
#define STACKINT_H_

#ifndef ALGO_H_
 #include "Algo.h"
 #define ALGO_H_
#endif /* !ALGO_H_ */

typedef struct StackInt StackInt;
struct StackInt
{
    char    _kooc__foobar_char;
    char    _kooc__foobar_int;

    int	    _kooc__size_int;
    int	    *_kooc__data_int_ptr;
};

void    _kooc_Stackint__foobar_void_Stackint_ptr(StackInt *self);

int     _kooc_StackInt_getSize_int_StackInt_ptr(StackInt *self);
void    _kooc_StackInt_init_void_StackInt_ptr_int(StackInt *self, int stackSize);
void    _kooc_StackInt_clean_void_StackInt_ptr(StackInt *self);
void    _kooc_StackInt_push_void_StackInt_ptr_int(StackInt *self, int newVal);
int     _kooc_StackInt_pop_int_StackInt_ptr(StackInt *self);
int     _kooc_StackInt_getMax_int_StackInt_ptr(StackInt *self);

StackInt    *_kooc_StackInt_alloc_StackInt_ptr_void();
StackInt    *_kooc_StackInt_new_StackInt_ptr_int(int stackSize);
void        _kooc_StackInt_delete_void_StackInt_ptr(StackInt *self);

extern int _kooc_Stackint_int_nbStack;

#endif /* STACKINT_H_ */
