#ifndef INHERITANCE_H_
#define INHERITANCE_H_

typedef struct _kooc_vtable_Animal
{
    void       (*_kooc_func_Animal_cry_void_0)();
}              _kooc_vtable_Animal;

typedef struct Animal Animal;
struct Animal
{
    _kooc_vtable_Animal *_kooc_vtable;
    int     _kooc_var__legs_int;
};

typedef struct _kooc_vtable_Cat
{
    _kooc_vtable_Animal _super;
}              _kooc_vtable_Cat;

typedef struct Cat Cat;
struct Cat
{
    Animal _super;
    _kooc_vtable_Cat *_kooc_vtable;
};

#endif /* !INHERITANCE_H_ */
