struct s_Test
{
  int a_int;
  char a_char;
  double a_double;

  int (*f_int)(int);
  char (*f_char)(char);
  void (*f_void)(int, char);
};

extern struct s_Test Test;
