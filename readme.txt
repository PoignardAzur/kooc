

















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
[static/inline/volatile/const]_{koocType/scalarType/ptr/tab$size}

ScalarType étant les types natifs (char, int ect..). En cas de type en deux mot (exemple long long) on les séparera par un ‘$’
kooType s’écrivant koocType_nom (exemple une classe kooc)
En cas de pointeurs ou de tableaux on relancera le processus de l’attribut sur le node suivant dans l’arbre.

Exemple : 

@module z
{
int a ; → _kooc_var_z_a_int
static int *a → _kooc_var_z_a_ptr_static_int
int volatile * static *const *a[4]  →
_kooc_var_z_a_volatile_ptr_static_ptr_const_ptr_tab-4_int
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
