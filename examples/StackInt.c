#include <stdlib.h>

#ifndef STACKINT_H_
#include "StackInt.h"
#define STACKINT_H_
#endif /* !STACKINT_H_ */

int     _KOOC_StackInt_IMPLEMENTATION;

int     _kooc_var_Stackint_nbStack_int = 0;

void    _kooc_func_Stackint__foobar_void_Stackint_ptr(StackInt *self)
{
}

int     _kooc_func_StackInt_getSize_int_StackInt_ptr(StackInt *self)
{
    return self->_kooc_var__size_int;
}

void    _kooc_func_StackInt_init_void_StackInt_ptr_int(StackInt *self, int stackSize)
{
    self->_kooc_var__size_int = stackSize;
    self->_kooc_var__data_int_ptr = (int *)calloc(stackSize, sizeof(int));
    ++_kooc_var_Stackint_nbStack_int;
}

void    _kooc_func_StackInt_clean_void_StackInt_ptr(StackInt *self)
{
    free(self->_kooc_var__data_int_ptr);
    --_kooc_var_Stackint_nbStack_int;
}

void    _kooc_func_StackInt_push_void_StackInt_ptr_int(StackInt *self, int newVal)
{
    ++self->_kooc_var__size_int;
    self->_kooc_var__data_int_ptr = (int *)realloc(self->_kooc_var__data_int_ptr, self->_kooc_var__size_int * sizeof(int));
    self->_kooc_var__data_int_ptr[self->_kooc_var__size_int - 1] = newVal;
}

int	    _kooc_func_StackInt_pop_int_StackInt_ptr(StackInt *self)
{
    int last = self->_kooc_var__data_int_ptr[self->_kooc_var__size_int - 1];

    --self->_kooc_var__size_int;
    self->_kooc_var__data_int_ptr = (int *)realloc(self->_kooc_var__data_int_ptr, self->_kooc_var__size_int * sizeof(int));
    return last;
}

int     _kooc_func_StackInt_getMax_int_StackInt_ptr(StackInt *self)
{
    return _kooc_func_Algo_greatest_int_2_arg_Pint_arg_int(self->_kooc_var__data_int_ptr, self->_kooc_var__size_int);
}

StackInt    *_kooc_StackInt_alloc_StackInt_ptr_void()
{
    return (StackInt *)malloc(sizeof(StackInt));
}

StackInt    *_kooc_StackInt_new_StackInt_ptr_int(int stackSize)
{
    StackInt *ptr = (StackInt *)malloc(sizeof(StackInt));
    _kooc_func_StackInt_init_void_StackInt_ptr_int(ptr, stackSize);
    return ptr;
}

void        _kooc_func_StackInt_delete_void_StackInt_ptr(StackInt *self)
{
    _kooc_func_StackInt_clean_void_StackInt_ptr(self);
    free(self);
}
