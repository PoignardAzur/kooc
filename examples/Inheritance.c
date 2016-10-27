#include <stdlib.h>

#ifndef INHERITANCE_H
#include "Inheritance.h"
#define INHERITANCE_H
#endif /* !INHERITANCE_H */

/*
** stdio.h code
** ...
*/

void _kooc_func_Animal_cry_void_1_arg_PSAnimal(Animal *self)
{
    printf("I have %d legs!\n", self->_kooc_var__legs_int);
}

_kooc_vtable_Animal _kooc_vtable_Animal_singleton =
{
    &_kooc_func_Animal_cry_void_1_arg_PSAnimal
};

void _kooc_func_Animal_init_void_2_arg_PSAnimal_arg_int(Animal *self, int legs)
{
    self->_kooc_vtable = &_kooc_vtable_Animal_singleton;
    self->_kooc_var__legs_int = legs;
}


void _kooc_func_Cat_cry_void_1_arg_PSCat(Cat *self)
{
    printf("Meow! I am a cat!\n");
}

_kooc_vtable_Cat _kooc_vtable_Cat_singleton =
{
    {
        &_kooc_func_Cat_cry_void_1_arg_PSCat
    }
};

void _kooc_func_Cat_init_void_1_arg_PSCat(Cat *self)
{
    self->_super._kooc_vtable = &_kooc_vtable_Cat_singleton._super;
    self->_kooc_vtable = &_kooc_vtable_Cat_singleton;
    self->_super._kooc_var__legs_int = 4;
}
