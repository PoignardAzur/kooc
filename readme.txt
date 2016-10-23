

















Kooc
Documentation















Groupe : Kooc aracha
Projet : KOOC – Kind of Objective C

Durée : 2 mois

Membres : timothee Le Gal de Kerangal, Gabriel Amice, Olivier Faure, Camille Priou, Louis Antonini, Xavier Loire

































Sommaire

Introduction
Conception générale
Compatibilité
Symbole mangling
Typage d’expression
Spécificité du langage
@import
@module
@implementation
@class
@member
synthaxe []
alloc, new, delete
@virtual
Conclusion




































Symbols Mangling

Le code du kooc doit pouvoir décorer les symbols dans les déclarations afin d’adapter un langage orienté objet au complitateur C

Le module de mangling va décorer les symboles de la façon suivante :

Note pour la notation : quand on a une alternative de mot clé obligatoire on notera l’alternative {mot clé1/mot clé2…}. Quand elle est optionelle on notera [mot clé1/mot clé2…] et on considerera qu’il peut se répéter jusqu’à ce qu’on ne rencontre un autre mot clé qui n’est pas dans le scope.

le caractère de séparation des différentes mot clés sera : _
le header d’un symbole sera _kooc suivis du type : var/func puis du nom du module ou de la classe : mod/class_name.

_kooc_{var/func}_{mod/classe_name}

La description d’un variable s’effectura de la manière suivante :

name_[attribut de type]_{type}

les attributs de types :
[static/inline/volatile/const]_{koocType/scalarType/ptr/tab$size/userdef$typename}

ScalarType étant les types natifs (char, int ect..). En cas de type en deux mot (exemple long long) on les séparera par un ‘’
En cas de présence d’un ‘_’ dans le nom d’un type ou de la variable on mettra ‘S’ devant
kooType s’écrivant koocType_nom (exemple une classe kooc)
En cas de pointeurs ou de tableaux on relancera le processus de l’attribut sur le node suivant dans l’arbre.
Quand le type est un user defined (structure, typedef) on mettra le préfix userdef puis un séparateur $ et le nom du type. En cas de structure on l’écrira dans le nom en le séparant par $

Exemple : 

@module z
{
int a ; → _kooc_var_z_a_int
static int *a → _kooc_var_z_a_ptr_static_int
int volatile * static *const *a[4]  →
_kooc_var_z_a_volatile_ptr_static_ptr_const_ptr_tab-4_int
struct s_e a ; → _kooc_var_z_a_userdef$struct$sS_e
}

La description des fonctions s’effectura de la manière suivante :

name_return_[attribut de type]_{type}_param_[void/[var]]]

Les paramètres seronts séparés par le mot clé : next. Si il y en aucun on mettra void
var se rapporte à la description d’une variable expliqué précédment

Exemple :

 @module z
{
	int	ft() → _kooc_func_z_ft_return_int_param_void
	int	*ft( static char a, const long long e) →  _kooc_func_z_ft_return_ptr_int_param_a_static_char_next_e_const_long$long
}
