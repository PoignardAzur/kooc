KOOC
====

Le KOOC est un langage de programmation compilé vers le C. L'exécutable "kooc" prend en paramètre des noms de fichiers .kh et .kc, et crée des fichiers .h et .c en sortie. Par exemple, la commande "kooc foo.kh bar.kc" créera les fichiers "foo.h" et "bar.c".


Les instructions KOOC
---------------------

Le langage KOOC est une surcouche du C. Les principaux ajouts sont les instructions KOOC, prenant la forme `@nom_de_la_declaration args...` suivie ou non d'un bloc. Sauf précision contraire, ces instructions se trouvent dans le scope global et ne peuvent pas être inclues dans un bloc, une structure, une fonction, etc.

Chaque fichier passé en paramètre du KOOC est "transformé" en un fichier lisible par un compilateur C. Les instructions en C ne sont pas modifiées, et sont inclues dans le fichier de sortie telles quelles. Chaque instruction KOOC est remplacée par une suite d'instructions C correspondante, et donne des informations supplémentaires au compilateur KOOC qui ne seront pas nécessairement ajoutées au fichier de sortie, mais seront utilisées pour des vérifications.

[NOTE: faire une règle pyrser demandant qu'il n'y ait rien d'autre sur la ligne? ex: ne pas autoriser `int x; @module` sur une seule ligne?]


L'instruction module
---------------------

Syntaxe:

`@module name_of_the_module { declarations... }`

Ce mot clé marque une définition du module name_of_the_module. Cette définition contient une suite de déclarations à la syntaxe KOOC, qui seront ajoutées à l'espace de nom name_of_the_module. Un module ne peut pas être défini plusieurs fois avec le même nom.

Une définition de module peut contenir des déclarations de variables et de fonctions. Plusieurs variables et fonctions du même nom, mais avec une signature différentes peuvent être déclarées. Lors de la conversion en C, leur nom sera décoré avec les informations de leur signature. La signature inclut le nom du module, le type d'une variable, le type de retour d'une fonction, et les types des arguments de la fonction. Si une variable ou fonction est déclarée comme étant statique, elle n'est pas déclarée dans le fichier en sortie.

NOTE: Autoriser les concaténations de modules?
NOTE: Autoriser les déclarations de types (typedef, struct, enum, etc)?
NOTE: Pas de inline?


L'instruction implementation
-----------------------------

Syntaxe:

`@implementation name_of_the_module { declarations... }`

Ce mot clé marque l'implémentation du module name_of_the_module. Il contient une suite de définitions de fonctions; chaque fonction inclue dans le bloc implementation doit avoir un prototype correspondant dans le bloc module. Les déclarations du bloc module qui impliquent une implémentation (ex: "int x = 3;") sont implicitement implémentées dans le fichier .c correspondant au bloc module.

Chaque bloc module doit avoir au plus un bloc implementation correspondant. Dans la mesure où plusieurs fichiers peuvent être compilés séparément, chacun implémentant le même module, ce qui mènerait à des erreurs de linkage difficiles à comprendre, l'implémentation d'un module crée un symbole KOOC_nom_du_module_IMPLEMENTATION, repérable dans les erreurs de linkage.

On peut imaginer une règle telle que les fonctions déclarées dans module, mais pas implémentées dans le bloc implementation déclencheraient un warning. On peut egalement imaginer un mot-clé `@implement_sup` qui contientrait des implémentations de fonctions déclarées dans le bloc module, mais n'incluerait pas d'implémentation implicite. Ce mot-clé permettrait de répartir l'implémentation d'un module sur plusieurs fichiers. Une autre solution pour pouvoir répartir l'implémentation sur plusieurs fichiers serait de ne pas mettre d'implémentation implicite dans le bloc implementation.


L'instruction import
---------------------

Syntaxe:

`@import "filename.kh"`

`@import modulename`

`@import classname`

Elle a deux effets: faire savoir au KOOC que les modules importés existent et sont appelables, et assurer l'inclusion par le code C compilé du contenu des modules/fichiers, en évitant les problèmes de double inclusion. L'instruction `import foobar` cherche dans tous les fichiers .kh et .kc le module ou la classe foobar. Les instructions `@implementation` et les opérateurs [] ne sont pas valides si ils ne sont pas précédés par une inclusion du module correspondant.

[NOTE chercher récursivement dans sous dossiers?]


L'instruction class
--------------------

Syntaxe:

`@class ClassName { declarations... }`

Cette déclaration est une surcouche de l'instructions module. Il créée un espace de nom ClassName, et les déclarations dans le bloc class sont gérées de la même façon que dans un bloc module. Le bloc de classe accepte également des déclarations `@member`, qui peuvent définir des variables ou des fonctions membres de ClassName. Lors de la compilation, une structure est créée, dont les champs sont les variables membres de la classe, et un typedef de cette structure est fait vers le nom de la classe. Les fonctions membres sont équivalentes à des fonctions de modules, avec un argument supplémentaire de type ClassName*.

L'implémentation d'une classe se fait à l'aide du mot-clé implementation, qui accepte également des déclarations member.

Syntaxe member:

`@member declaration`

`@member { declarations... }`


Opérateur '[]'
--------------

Syntaxes:

`[modulename.varname]`

`@!(type_name)[modulename.varname]`

`[modulename funcname : arg1 : arg2 : ...]`

`@!(type1)[modulename funcname : arg1 : "@!(type2)arg2 : ...]` (à vérifier)

`[object funcname : args...]`

`[object.varname]`

Récupère la variable ou exécute la fonction définie dans modulename (modulename peut être une classe). Le type de retour peut être inféré par le compilateur ou précisé par l'utilisateur. Un type ambigu est une erreur de compilation.

Les deux dernières syntaxe est valide seulement si il existe une classe `ClassName` telle que `object` est de type `ClassName *`. Elle est équivalente à `[ClassName funcname : object : args...]`.

[NOTE: qu'est-ce qui se passe si object est une expression?]
TODO - Ajouter new/init/delete/alloc

[NOTE: espaces avant/après ':']
[NOTE: ": arg1 : arg2" ou ": arg1 arg2"]
