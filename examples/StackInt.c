#include <stdlib.h>

#ifndef STACKINT_H_
#include "StackInt.h"
#define STACKINT_H_
#endif /* !STACKINT_H_ */

int _kooc_Stackint_int_nbStack = 0;

void    _kooc_Stackint__foobar_void_Stackint_ptr(StackInt *self)
{
}

int     _kooc_StackInt_getSize_int_StackInt_ptr(StackInt *self);
{
    return self->_size;
}

void	_kooc_StackInt_init_void_StackInt_ptr_int(StackInt *self, int stackSize);
{
    self->_size = size;
    self->_data = (int *)calloc(size, sizeof(int));
    ++_kooc_Stackint_int_nbStack;
}

void	_kooc_StackInt_clean_void_StackInt_ptr(StackInt *self);
{
    free(self->_data);
    --_kooc_Stackint_int_nbStack;
}

void    _kooc_StackInt_push_void_StackInt_ptr_int(StackInt *self, int newVal);
{
    ++self->_size;
    self->_data = (int *)realloc(self->_data, size * sizeof(int));
    self->_data[self->_size - 1] = newVal;
}

int	    _kooc_StackInt_pop_int_StackInt_ptr(StackInt *self)
{
    int last = self->_data[self->_size - 1];

    --self->_size;
    self->_data = (int *)realloc(self->_data, size * sizeof(int));
    return last;
}

int     _kooc_StackInt_getMax_int_StackInt_ptr(StackInt *self)
{
    return _kooc_Algo_greatest_int_int_int(self->_data, self->_size);
}

StackInt    *_kooc_StackInt_alloc_StackInt_ptr_void()
{
    return (StackInt *)malloc(sizeof(StackInt));
}

StackInt    *_kooc_StackInt_new_StackInt_ptr_int(int stackSize)
{
    StackInt ptr = (StackInt *)malloc(sizeof(StackInt));
    _kooc_StackInt_init_void_StackInt_ptr_int(ptr, stackSize);
    return ptr;
}

void        _kooc_StackInt_delete_void_StackInt_ptr(StackInt *self)
{
    _kooc_StackInt_clean_void_StackInt_ptr(self);
    free(self);
}
