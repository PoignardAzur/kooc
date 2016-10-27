KOOC
====

*Groupe:* Kooc aracha

*Projet:* KOOC – Kind of Objective C

*Durée:* 2 mois

*Membres:* Timothee Le Gal de Kerangal, Gabriel Amice, Olivier Faure, Camille Priou, Louis Antonini, Xavier Loire.

Le KOOC est un langage de programmation compilé vers le C. L'exécutable `kooc` prend en paramètre des noms de fichiers .kh et .kc, et crée des fichiers .h et .c en sortie. Par exemple, la commande `kooc foo.kh bar.kc` créera les fichiers `foo.h` et `bar.c`.

Le KOOC est un langage de programmation compilé vers le C. L'exécutable `kooc` prend en paramètre des fichiers de texte écrite en langage KOOC, analyse ces fichiers, et crée des fichiers correspondants en langage C, capables d'être lus par le compilateur `gcc`, et exécutant les tâches décrites dans les fichiers KOOC. Ce procédé, similaire aux origines du C++, permet de générer mécaniquement du code C ayant des propriétés étrangères au langages.


Les fonctionnalités du KOOC
---------------------------

Le langage KOOC a pour but d'implémenter les fonctionnalités de bases d'un langage orienté objet:

* Création d'espaces de nom (les modules)

* Surcharge de fonctions

* Création de types abstraits de données (ADT), possédant des méthodes et une durée de vie.

* Système d'héritage, et d'héritage virtuel, permettant la création de collections hétérogènes


La syntaxe KOOC
===============

Les fonctionnalités du KOOC sont implémentées à travers une surcouche du C, ce qui signifie que tout code valide en C est également valide en KOOC. À l'inverse du C++, qui réutilise des constructions syntaxiques illégales en C et leur donne un sens nouveau, les instructions ajoutées par le KOOC utilisent leur propre syntaxe distincte du C.

Les principaux ajouts sont les instructions KOOC, prenant la forme `@nom_de_la_declaration args...` suivie ou non d'un bloc. Sauf précision contraire, ces instructions se trouvent dans le scope global et ne peuvent pas être positionnées dans un bloc, une structure, une fonction, etc. Chaque instruction KOOC est remplacée par une suite d'instructions C correspondante, et donne des informations supplémentaires au compilateur KOOC qui ne seront pas nécessairement ajoutées au fichier de sortie, mais seront utilisées pour des vérifications (ex: vérifier qu'un appel KOOC fait bien référence à un fonction déclarée plus haut). Le code C en dehors de ces instructions n'est pas modifié, à l'exception des appels KOOC (Voir Opérateur `[]`).


L'instruction module
---------------------

Syntaxe:

`@module name_of_the_module { declarations... }`

Cette instruction marque la définition du module `name_of_the_module`. Cette définition contient une suite de déclarations en C, qui seront ajoutées à l'espace de nom name_of_the_module. Un module ne peut pas être défini plusieurs fois avec le même nom.

Une définition de module peut contenir des déclarations de variables et de fonctions. Plusieurs variables et fonctions du même nom mais avec une signature différentes peuvent être déclarées. Lors de la conversion en C, leur nom sera décoré avec les informations de leur signature (Voir Décoration de symboles); ce mécanisme est nommé la surcharge de variable/fonction. La signature inclut le nom du module, le type d'une variable, le type de retour d'une fonction, et les types des arguments de la fonction. Si une variable ou fonction est déclarée comme étant statique, elle n'est pas déclarée dans le fichier en sortie.

Exemple:

    @module Universe
    {
        int     THE_ANSWER = 42;
        char    THE_ANSWER = 42;

        int     return_the_answer();
    }

Deviendra:

`extern int      _kooc_var_Universe_THE_ANSWER_int;`
`extern char     _kooc_var_Universe_THE_ANSWER_char;`

`int             _kooc_func_Universe_return_the_answer_int_0();`

*NOTE:* Si une déclaration de type (ex: typedef, struct, enum, etc) est inclue dans un bloc de module, on peut imaginer plusieurs façon de la gérer: l'inclure dans le code C sans la décorer (et éventuellement inclure un warning), arrêter la compilation et afficher un message d'erreur, ou décorer la déclaration, et prévoir une syntaxe KOOC pour accéder au type. La seconde solution est celle qui demande le moins d'efforts; l'inconvénient de la première solution est qu'elle peut mener à des erreurs contre-intuitives, si deux types différents, mais ayant le même nom sont déclarés dans deux modules différents.

*NOTE:* Il est possible que la définition d'un module accepte des implémentations de fonctions en plus des simples prototypes. Dans ce cas là, la déclaration de la fonction devrait être précédée du mot-clé `inline`; dans le cas contraire le compilateur pourra émettre une erreur ou un warning.


L'instruction implementation
-----------------------------

Syntaxe:

`@implementation name_of_the_module { declarations... }`

Cette instruction marque l'implémentation du module name_of_the_module. Il contient une suite de définitions de fonctions; chaque fonction inclue dans le bloc implementation doit avoir un prototype correspondant dans le bloc module. Les déclarations du bloc module qui impliquent une implémentation (ex: "int x = 3;") sont implicitement implémentées dans le fichier .c correspondant au bloc module.

Chaque bloc module doit avoir au plus un bloc implementation correspondant. Dans la mesure où plusieurs fichiers peuvent être compilés séparément, chacun implémentant le même module, ce qui mènerait à des erreurs de linkage difficiles à comprendre, l'implémentation d'un module crée un symbole `_KOOC_nom_du_module_IMPLEMENTATION`, repérable dans les erreurs de linkage.

Exemple:

    @implementation Universe
    {
        int         return_the_answer()
        {
            return 42;
        }
    }

Deviendra:

    `int      _KOOC_Universe_IMPLEMENTATION;`
    `int      _kooc_var_Universe_THE_ANSWER_int = 42;`
    `char     _kooc_var_Universe_THE_ANSWER_char = 42;`

    `int      _kooc_func_Universe_return_the_answer_int_0()`
    {
        return 42;
    }

NOTES: On peut imaginer une règle telle que les fonctions déclarées dans module, mais pas implémentées dans le bloc implementation déclencheraient un warning. On peut egalement imaginer un mot-clé `@implement_sup` qui contientrait des implémentations de fonctions déclarées dans le bloc module, mais n'incluerait pas d'implémentation implicite. Ce mot-clé permettrait de répartir l'implémentation d'un module sur plusieurs fichiers. Une autre solution pour pouvoir répartir l'implémentation sur plusieurs fichiers serait de ne pas mettre d'implémentation implicite dans le bloc implementation.


L'instruction import
---------------------

Syntaxe:

`@import "filename.kh"`

Cette instruction a deux effets: faire savoir au KOOC que les modules importés existent et sont appelables, et assurer l'inclusion par le code C compilé du contenu des modules/fichiers, en évitant les problèmes de double inclusion. Les instructions `@implementation` et les opérateurs [] ne sont pas valides si ils ne sont pas précédés par une inclusion du module correspondant.

Exemple:

    @import "ThisTeamIsReallyGoodAndIShouldGiveThemAGoodGrade.kh"

Deviendra:

    #ifndef THISTEAMISREALLYGOODANDISHOULDGIVETHEMAGOODGRADE_H_
     #include "ThisTeamIsReallyGoodAndIShouldGiveThemAGoodGrade.h"
     #define THISTEAMISREALLYGOODANDISHOULDGIVETHEMAGOODGRADE_H_
    #endif // !THISTEAMISREALLYGOODANDISHOULDGIVETHEMAGOODGRADE_H_

*NOTE:* Les fichiers .h générés par `kooc` sont automatiquement protégés contre la double inclusion, au cas où ils seraient inclus par un fichier C. Pour cette raison, la directive `#define` est placée après la directive `#include`.

*NOTE:* Par défaut, le compilateur interprète l'addresse donnée comme étant relative au dossier du fichier compilé. Si le fichier `dir1/foo.kc` comprend une instruction `import "subdir/bar.kh"`, le compilateur cherchera le fichier à l'addresse `dir1/subdir/bar.kh`. Si le programme a été lancé avec un ou plusieurs arguments `-I dirname`, le compilateur essaie d'abord d'interpréter les addresse données par import comme étant relative à chacun des dossiers passés en argument, par ordre de passage.


L'instruction class
--------------------

Syntaxe:

`@class ClassName { declarations... }`

Cette instruction crée un espace de nom `ClassName`; les déclarations dans le bloc `class` sont traitées de la même façon que dans un bloc `module`. Le bloc de classe accepte également des déclarations `@member`, qui peuvent définir des variables ou des fonctions membres de `ClassName`. Lors de la compilation, une structure est créée, dont les champs sont les variables membres de la classe, et un typedef de cette structure est fait vers le nom de la classe.

Les fonctions membres d'une classe sont strictement équivalentes à des fonctions de modules, avec un argument supplémentaire de type `ClassName*`. Une fonction membre `int foobar(int x)` est une fonction non-membre `int foobar(ClassName* self, int x)` peuvent être appelées de la même façon, et ont la même signature; la seule exception à cette règle est le cas des fonctions membres virtuels (Voir Méthodes virtuelles).

L'implémentation des méthodes d'une classe se fait à l'aide du mot-clé `@implementation`, qui accepte également des déclarations `@member`.

Pour un exemple de création de classe, voir `examples/StackInt.*`.

Syntaxe `@member`:

`@member declaration`

`@member { declarations... }`

*NOTE:* Les variables membres sont également appelées attributs, et les fonctions membres sont également appelées méthodes.


Fonctions spéciales
-------------------

Les fonctions suivantes ont une sémantique propre dans le contexte d'une classe: `init`, `alloc`, `new`, `clean`, et `delete`.

### Les fonctions `init`, `alloc` et `new`

La méthode `init` est un constructeur, et doit être appelée à l'instanciation d'une classe. En écrivant une classe, le codeur peut définir autant de méthodes nommées `init` qu'il le souhaite, en utilisant les mécanismes de surcharge de fonction. Si aucun constructeur n'est défini, le KOOC en génère un par défaut, qui initialise tous les champs soit à zéro, soit à leur valeur indiquée dans la déclaration; par exemple, si un attribut est déclaré sous la forme `@member int x = 333`, alors le constructeur par défaut initialisera la valeur de x à 333. Il est possible d'accéder au constructeur par défaut depuis un autre constructeur avec la syntaxe `[super init]` (Voir Résolution de types).

La fonction non-membre `alloc` est générée automatiquement pour chaque classe. Elle alloue un bloc de mémoire de la taille de la classe, et est équivalente à `malloc(sizeof(ClassName))`. La fonction non-membre `new` est générée automatiquement, et appelle la fonction `alloc`, puis la fonction `init`. Le KOOC génère autant de surcharges de la fonction `new` qu'il y a de surcharges de la fonction `init`. Essayer de surcharger `alloc` ou `new` déclenche une erreur.

### Les méthodes `clean` et `delete`

La méthode `clean` est optionnellement écrite par l'utilisateur, et ne doit prendre aucun paramètre. Cette méthode est le destructeur de la classe, et doit libérer les ressources allouées par une instance. La méthode `delete` appelle la méthode `clean` si elle existe, puis libère l'espace mémoire de l'objet. Essayer de surcharger `delete` déclenche une erreur.

Si une classe est codée sans destructeur, mais possède des attributs qui en ont un, alors un destructeur est automatiquement généré; ce destructeur appelle simplement les destructeur de chacun des attributs de l'instance.

Lorsqu'une classe possédant un destructeur est instanciée dans une fonction, le destructeur de l'instance est automatiquement appelé juste avant la fin de la portée de cette classe.

Exemple:

    int foobar()
    {
        MyClass abc;

        ...
        return 0;
    }

Deviendra:

    int foobar()
    {
        MyClass abc;

        ...
        MyClass_clean_void_MyClass_ptr(&abc);
        return 0;
    }


Opérateur `[]`
--------------

Syntaxes:

`[Foobar.varname]`

`@!(type_name)[Foobar.varname]`

`[Foobar funcname : arg1 : arg2 : ...]`

`@!(type1)[Foobar funcname : arg1 : @!(type2)arg2 : ...]`

L'opérateur `[]`, ou appel KOOC, permet d'accéder aux fonctions et variables d'un module ou d'une classe à l'intérieur d'une instruction C.

L'appel `[Foobar.varname]` récupère la variable `varname` définie dans l'espace de nom `Foobar`, qui peut être un module ou une classe. Si l'espace de nom possède plusieurs surcharges de la variable `varname`, la variable récupérée est celle ayant le type attendu par l'appel. Ce type est inféré par le compilateur en fonction du contexte entourant l'appel (par exemple, `int x = [Foobar.varname]` recupèrera la surcharge de `var` de type `int`); il peut également être précisé par l'utilisateur avec la syntaxe `@!(type_name)[Foobar.varname]`. Si le type de l'appel n'est pas précisé, et il est impossible de le déduire du contexte, alors la compilation s'arrête sur une erreur (Voir Résolution de types).

L'appel `[Foobar funcname]` récupère la fonction sans arguments `funcname` de l'espace de nom `Foobar`. L'appel `[Foobar funcname : arg1 : arg2]` récupère la fonction `funcname` à deux arguments. L'appel `@!(type1)[Foobar funcname : arg1 : @!(type2)arg2]` précise en plus le type de retour et le type du second argument attendus. (Voir Résolution de types)

Si l'appel KOOC est situé dans le corps de l'implémentation d'une fonction membre, alors il donne une sémantique spéciale aux identifiants `self` et `super`. L'id `self` est interprété comme un pointeur sur l'instance appelante de la classe, et l'id `super` comme étant un pointeur sur cette même instance, interprété comme étant du type parent (Voir Héritage).

A la compilation, l'appel KOOC est remplacé par l'expression C correspondante; dans le cas d'un appel de variable, le nom décoré de la variable; dans le cas d'un appel de fonction, le nom décoré de la fonction, avec ses arguments.

Exemple:

`int var = @!(long)[Algo greatest : @!(long *)my_array : 10];`

Deviendra:

    `int var = _kooc_func_Algo_greatest_long_2_arg_long_arg_Pint(my_array, 10);`

*NOTE:* Dans le cas où une variable et une fonction sont déclarées avec le même nom, il est possible d'accéder à la variable, ou à la fonction, selon la syntaxe utilisée. Il est en revanche impossible d'accéder à l'addresse de la fonction; ce problème pourrait être résolu en ajoutant une syntaxe (ex: `[Module.&funcame]`) récupérant spécifiquement l'addresse d'une fonction.

### La syntaxe orientée objet

Syntaxes:

`[object.varname]`

`[object funcname : args...]`

Ces deux syntaxes sont valides seulement si `object` est un pointeur sur une classe qui possède un membre `funcname`/`varname`.

La première syntaxe est équivalente à `object->mangled_varname`, où `mangled_varname` correspond au nom décoré de `varname`, selon les mêmes règles que pour un appel de variable non membre.

La second syntaxe a deux sémantiques différentes. Si `funcname` est une méthode non virtuelle, alors cette syntaxe est strictement équivalente à `[ClassName funcname : object : args...]`, où `ClassName` est le type de `object`. Si `funcname` est une méthode virtuelle, alors cette syntaxe n'appelle pas la fonction définie dans l'espace de nom `ClassName`, mais la fonction correspondante, à l'addresse de la table virtuelle de `object`. (Voir Méthodes virtuelles)

*NOTE:* Par défaut, ces syntaxes n'acceptent qu'un nom de variable de type `ClassName *`. Cette approche a l'avantage d'être simple à implémenter, et ne laisser aucune confusion possible. Cependant, elle manque de flexibilité, et oblige le programmeur à déclarer un pointeur pour chaque cas où l'adresse de `object` est calculée, ce qui ne permet pas des raccourcis simples comme `[&object.varname]`. La solution la plus simple pour ce problème est de rajouter un cas spécial pour `&object`. Une autre solution serait d'autoriser object à être n'importe quelle expression ayant pour type `ClassName *`; cette solution serait plus complexe à implémenter, et créerait des cas où l'interprétation d'une instruction serait visuellement ambiguë. Une autre solution serait de créer une syntaxe spécifique, et non ambiguë, pour la gestion d'une instance d'objet.


Héritage
--------

Syntaxe:

`class ClassName(ParentName) { declarations... }`

Cette syntaxe permet de faire hériter `ClassName` d'une classe `ParentName` précédemment définie. On dit que `ClassName` est la classe fille de `ParentName`, et que `ParentName` est la classe parente de `ClassName`. Tous les attributs et les méthodes de `ParentName` sont accessibles depuis `ClassName`. Par exemple, si `ParentName` possède une méthode `foo()` et un attribut `bar`, alors `[ClassName foo : obj]` et `[obj.bar]` sont des appels valides si `obj` est de type `ClassName *`. Une fois compilé en code C, la première variable stockée dans la structure `ClassName` est une instance de `ParentName`; cela permet d'utiliser un pointeur sur `ClassName` comme étant un pointeur sur `ParentName`.

En plus de l'identifiant `super`, une méthode `super` sans arguments est générée automatiquement dans la classe fille, qui renvoie l'instance appelante typée comme étant de la classe parente.

Pour un exemple d'utilisation d'héritage, voir `examples/Inheritance.*` et `examples/main.*`.

### Méthodes virtuelles

Syntaxe:

`@virtual declaration`

Exemple:

`@member @virtual int foobar();`

Le mot-clé `@virtual` signale qu'une méthode est virtuelle. Lorsqu'une classe a au moins une méthode virtuelle, une table virtuelle, ou vtable, est générée pour cette classe. La vtable est une structure contenant des pointeurs sur chaque méthode virtuelle de la classe. Des instances de cette structure sont créées pour la classe et chacune de ses classes filles. Si une méthode est redéfinie dans une classe fille, alors le pointeur sur fonction correspondant dans l'instance de la vtable de la classe fille pointera sur la méthode redéfinie. La mot clé `@virtual` ne peut être placé que dans un bloc de classe; il ne peut pas être placé dans un bloc d'implémentation.

L'appel d'une méthode virtuelle peut se faire de deux façons différentes. La syntaxe `[ClassName foobar : object : args...]` fait directement appel à la méthode définie dans l'espace de nom `ClassName`, et n'utilise pas la vtable. La syntaxe `[object foobar : args...]`, en revanche, fait appel à la fonction à l'addresse pointée par l'attribut `foobar` de la vtable de `object`; cette syntaxe est équivalente à `object->vtable->foobar_with_mangling(object, args...)`, et appelle la méthode correspondant au type réel de `object`, et non le type de sa référence.

Si une classe a au moins une méthode virtuel, alors son destructeur est automatiquement déclaré comme étant virtuel. Cela permet par exemple de stocker des collections de pointeurs sur une classe parente, et, a la destruction de cette collection, d'appeller tous les destructeurs des classes filles réelles des objets de la collections.

Déclarer un constructeur, un attribut ou une fonction non-membre comme étant virtuel est une erreur de compilation.

*NOTE:* On peut prévoir un cas particulier où la syntaxe `[&obj func : args]` est utilisée, et `obj` est une variable de type `ClassName`; dans ce cas, le type de `&obj` serait connu à la compilation et l'utilisation de la vtable pourrait être omise.


Fonctionnement du compilateur
=============================

Le projet entier est codé en Python. L'exécutable `kooc` prend en paramètre des chemins de fichiers ayant les extensions .kh et .kc et contenant du code KOOC, traduit ce code en code C pour chaque fichier, et crée des fichiers .h et .c correspodants en sortie.

Par exemple, la commande

`kooc foo.kh bar.kc`

Créera les fichiers

`foo.h bar.c`.

L'exécutable peut également prendre en paramètre des arguments sous la forme `-I dirname`, qui ajoutent des addresses de dossier à partir desquels chercher les directives `@import` (Voir L'instruction import).


Étapes de compilation
---------------------

La compilation de chaque fichier est séparée en plusieurs étapes, ou passes. Chaque passe transforme l'état des données du fichier en un objet lisible par la passe suivante, jusqu'à ce que le code KOOC soit transformé en code C. Les ressources utilisées par chaque passe sont détaillées dans les sections à venir. Les passes sont les suivantes:

* Parser le fichier KOOC. Cette passe transforme le texte au format KOOC en un AST KOOC (Voir L'arbre généré). Elle doit aussi lister tous les types et les objets déclarés dans le fichier, et les fichiers qu'il importe.

* Remplacer les appels KOOC par des instructions C. Cette passe parcours l'AST KOOC, et transforme chaque appel KOOC (syntaxe `[]`) en une instruction C correspondante, en résolvant les types de l'appel et en appliquant la décoration de symboles.

* Transformer chaque déclaration KOOC en déclarations C. Cette passe transforme l'AST KOOC en un AST C lisible par CNorm. Elle parcourt l'AST et remplace chaque déclaration KOOC par une liste de déclarations C, en décorant les symboles et en appliquant des règles spécifiques à chaque déclaration (Voir La Syntaxe KOOC).

* Transformer l'AST C en code C. Cette passe est un simple appel à la méthode `to_c` de CNorm.

Pour plus de détails sur les passes du compilateur, voir `Compiling_FAST.pdf`.


Le parsing
----------

Le parsing est fait avec les modules CNorm et (indirectement) Pyrser. L'arbre de syntaxe est généré par une classe `KoocParser`, dans le module éponyme, qui hérite de la classe `Declaration` de CNorm et de ses méthodes `parse` et `parse_file`. La classe `KoocParser` définit la syntaxe du KOOC, sous forme d'une BNF Pyrser identique à celle présente dans le fichier `KOOC_Syntax.bnf`, et de hooks contruisant l'AST des déclarations et appels KOOC.

Les hooks de `KoocParser` doivent également construire une liste de types et d'objets à utiliser pour la résolution d'appels KOOC (Voir Résolution de types).


L'arbre généré
--------------

La méthode `parse()` de `KoocParser` renvoit un objet `Node`. Cet objet a un attribut `types`, qui est une liste de types déclarés dans le fichier compilé, un attribut `objects` et un attribut `body`, qui est une liste mixte de déclarations C, et de déclarations KOOC, et qui correspond à la liste des déclarations du fichier. Une déclaration KOOC peut être un des objets suivants:

    KoocImport
        filename    : str

    KoocModule
        name        : str
        fields      : List<cnorm.nodes.Decl>

    KoocClass
        name        : str
        fields      : List<cnorm.nodes.Decl>
        members     : List<KoocMember>

        KoocMember
            isVirtual   : bool
            decl        : cnorm.nodes.Decl

    KoocImplem
        name        : str
        fields      : List<cnorm.nodes.Decl>        >> Implémentations de fonctions

Le parseur peut également trouver des appels KOOC à l'intérieur des expressions C. Ces appels KOOC sont stockés à l'intérieur des AST de déclarations C sous la forme suivante:

    KoocCall
        target      : str || cnorm.nodes.Expr       >> Espace de nom ou instance de classe
        name        : str
        isFunc      : bool
        args        : None || List<cnorm.nodes.Expr>


Décoration de symboles
----------------------

Le langage KOOC permet la surcharge de variables et de fonctions. Deux modules différents peuvent posséder une variable du même nom, et un module peut posséder deux variables du même nom mais de types différents, et ces variables produiront des symboles lisibles par un compilateur C. Ceci est accompli à travers la décoration de symbole: chaque objet déclaré dans un module ou une classe KOOC voit son nom changé, pour produire un nom unique dans le code C résultant. Ce code est obtenu en ajoutant au du texte obtenu à partir de la signature de la variable/fonction.

La signature d'un objet inclut son type (variable ou fonction), l'espace de nom dans lequel il se trouve, son type de retour, et ses arguments. Les symboles sont décorés selon le format suivant:

`_kooc_var_NAMESPACE_VARNAME_TYPE`
`_kooc_func_NAMESPACE_FUNCNAME_RETURNTYPE_0`
`_kooc_func_NAMESPACE_FUNCNAME_RETURNTYPE_ARGCOUNT[_arg_ARGTYPE]*`

Dans ce format, TYPE, ARGTYPE et RETURNTYPE font référence à des chaines décrivant un type. Ces chaines sont les suivantes:

| Type                                                                   | Chaine correspondante |
|------------------------------------------------------------------------|-----------------------|
| char                                                                   | char                  |
| signed char                                                            | schar                 |
| unsigned char                                                          | uchar                 |
| short && short int && signed short && signed short int                 | short                 |
| unsigned short && unsigned short int                                   | ushort                |
| int && signed && signed int                                            | int                   |
| unsigned && unsigned int                                               | uint                  |
| long && long int && signed long && signed long int                     | long                  |
| unsigned long && unsigned long int                                     | ulong                 |
| long long && long long int && signed long long && signed long long int | llong                 |
| unsigned long long && unsigned long long int                           | ullong                |
| float                                                                  | float                 |
| double                                                                 | double                |
| long double                                                            | ldouble               |
| TYPENAME*                                                              | PTYPENAME             |
| TYPENAME[42]                                                           | A42TYPENAME           |
| struct TYPENAME                                                        | STYPENAME             |
| enum TYPENAME                                                          | ETYPENAME             |
| union TYPENAME                                                         | UTYPENAME             |

La décoration d'un type déclaré par un typedef est la même que celle du type originel. La décoration d'un type pointeur sur fonction est la suivante:

`FRETURNTYPE_ARGCOUNT[_arg_ARGTYPE]*`

La signature d'un objet ne change pas qu'il soit ou non déclaré comme étant statique, inline, constant, volatile, ou extern. Ainsi, la déclarations suivante est une erreur de compilation:

    @module M
    {
        static int x;
        const int x;
    }

Des exemples de décorations de symboles se trouvent dans les fichiers de traduction dans `examples/*.c examples/*.h`.

*NOTE:* Ces fichiers d'exemples ayant été écrits à la main et non mécaniquement, il est possible que certains des décorations dans ces fichiers soient invalides.


Résolution de types
-------------------

La surcharge de variables/fonctions implique une ambiguité possible lors des appels KOOC. Par exemple, dans le code suivant:

    @module Foobar
    {
        int x;
        char x;
    }

    int fbx = [Foobar.x];

L'appel `[Foobar.x]` correspond-il à la première ou la seconde déclaration de `x`? Cette ambiguité peut être résolu par un précision manuelle des types attendus (Voir Opérateur []), ou par une résolution à la compilation des types. Dans l'exemple précédent, `Foobar.x` est assigné à un `int`, le compilateur peut donc en déduire que la variable attendue est celle déclarée dans `Foobar` comme étant un `int`.

L'algorithme de résolution de types pour un appel `[Foobar.func : args...]` est le suivant:

* Si l'appel KOOC est situé dans une opération (ex: `[Foobar.func : args...] + 3`), l'agorithme est appliqué à cette opération.

* Une liste de toutes les fonctions `func` dans le module `Foobar` ayant le nombre d'arguments de `args...` est faite.

* Les types de renvoi ou d'arguments précisés par l'utilisateur sont fixés. Les fonctions n'ayant pas ces types de renvoi / d'arguments sont éliminées de la liste.

* Si l'appel KOOC est situé dans une assignation (ex: `int fbx = [Foobar.x];`), le type de renvoi est fixé.

* Pour chaque argument dans `arg`, une liste de types de retour possibles est générée. Si l'argument est une expression C, on tente de déterminer son type. Si l'argument est un appel KOOC, cet algorithme lui est appliqué pour générer la liste, avec comme contrainte que le type de retour de l'appel KOOC doit être un des types acceptés en paramètre par la les fonctions `func` restantes.

* Les fonctions dont au moins un argument n'est pas dans la liste de retours possibles sont supprimées de la liste. Si la liste a été réduite, on ré-applique l'étape précédente.

* La liste des fonctions restantes est renvoyée. Si cette liste n'est pas composée d'un seul élément, et l'appel de cet algorithme n'est pas récursif, alors le type de la fonction est ambigu, et une erreur de compilation est déclenchée.

*NOTE:* Cet algorithme part du principe que les types sont comparables seulement en termes d'égalité/inégalité, et ne prend pas en compte les conversions implicites ou l'héritage. On peut concevoir un algorithme plus complexe qui classerait les types par ordre de conversion (par exemple, int est convertible en long, mais pas l'inverse), et ajouter des passes supplémentaires pour en tenir compte. Cependant, l'agorithme présent répond aux besoins de base du projet.
