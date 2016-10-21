KOOC
====

Le KOOC est un langage de programmation compilé vers le C. L'exécutable "kooc" prend en paramètre des noms de fichiers .kh et .kc, et crée des fichiers .h et .c en sortie. Par exemple, la commande "kooc foo.kh bar.kc" créera les fichiers "foo.h" et "bar.c".


Les instructions KOOC
---------------------

Le langage KOOC est une surcouche du C. Les principaux ajouts sont les instructions KOOC, prenant la forme `@nom_de_la_declaration args...` suivie ou non d'un bloc. Sauf précision contraire, ces instructions se trouvent dans le scope global et ne peuvent pas être inclues dans un bloc, une structure, une fonction, etc.

Chaque fichier passé en paramètre du KOOC est "transformé" en un fichier lisible par un compilateur C. Les instructions en C ne sont pas modifiées, et sont inclues dans le fichier de sortie telles quelles. Chaque instruction KOOC est remplacée par une suite d'instructions C correspondante, et donne des informations supplémentaires au compilateur KOOC qui ne seront pas nécessairement ajoutées au fichier de sortie, mais seront utilisées pour des vérifications.


L'instruction module
---------------------

Syntaxe:

`@module name_of_the_module { declarations... }`

Cette instruction marque une définition du module name_of_the_module. Cette définition contient une suite de déclarations à la syntaxe KOOC, qui seront ajoutées à l'espace de nom name_of_the_module. Un module ne peut pas être défini plusieurs fois avec le même nom.

Une définition de module peut contenir des déclarations de variables et de fonctions. Plusieurs variables et fonctions du même nom, mais avec une signature différentes peuvent être déclarées. Lors de la conversion en C, leur nom sera décoré avec les informations de leur signature. La signature inclut le nom du module, le type d'une variable, le type de retour d'une fonction, et les types des arguments de la fonction. Si une variable ou fonction est déclarée comme étant statique, elle n'est pas déclarée dans le fichier en sortie.

NOTE: Si une déclaration de type (ex: typedef, struct, enum, etc) est inclue dans un bloc de module, on peut imaginer plusieurs façon de la gérer: l'inclure dans le code C sans la décorer (et éventuellement inclure un warning), arrêter la compilation et afficher un message d'erreur, ou décorer la déclaration, et prévoir une syntaxe KOOC pour accéder au type. La seconde solution est celle qui demande le moins d'efforts; l'inconvénient de la première solution est qu'elle peut mener à des erreurs contre-intuitives, si deux types différents, mais ayant le même nom sont déclarés dans deux modules différents.

NOTE: Il est possible que la définition d'un module accepte des implémentations de fonctions en plus des simples prototypes. Dans ce cas là, la déclaration de la fonction devrait être précédée du mot-clé `inline`; dans le cas contraire le compilateur pourra émettre une erreur ou un warning.


L'instruction implementation
-----------------------------

Syntaxe:

`@implementation name_of_the_module { declarations... }`

Cette instruction marque l'implémentation du module name_of_the_module. Il contient une suite de définitions de fonctions; chaque fonction inclue dans le bloc implementation doit avoir un prototype correspondant dans le bloc module. Les déclarations du bloc module qui impliquent une implémentation (ex: "int x = 3;") sont implicitement implémentées dans le fichier .c correspondant au bloc module.

Chaque bloc module doit avoir au plus un bloc implementation correspondant. Dans la mesure où plusieurs fichiers peuvent être compilés séparément, chacun implémentant le même module, ce qui mènerait à des erreurs de linkage difficiles à comprendre, l'implémentation d'un module crée un symbole KOOC_nom_du_module_IMPLEMENTATION, repérable dans les erreurs de linkage.

NOTES: On peut imaginer une règle telle que les fonctions déclarées dans module, mais pas implémentées dans le bloc implementation déclencheraient un warning. On peut egalement imaginer un mot-clé `@implement_sup` qui contientrait des implémentations de fonctions déclarées dans le bloc module, mais n'incluerait pas d'implémentation implicite. Ce mot-clé permettrait de répartir l'implémentation d'un module sur plusieurs fichiers. Une autre solution pour pouvoir répartir l'implémentation sur plusieurs fichiers serait de ne pas mettre d'implémentation implicite dans le bloc implementation.


L'instruction import
---------------------

Syntaxe:

`@import "filename.kh"`

Cette instruction a deux effets: faire savoir au KOOC que les modules importés existent et sont appelables, et assurer l'inclusion par le code C compilé du contenu des modules/fichiers, en évitant les problèmes de double inclusion. Les instructions `@implementation` et les opérateurs [] ne sont pas valides si ils ne sont pas précédés par une inclusion du module correspondant.

NOTE: Par défaut, le compilateur interprète l'addresse donnée comme étant relative au dossier du fichier compilé. Si le fichier `dir1/foo.kc` comprend une instruction `import "subdir/bar.kh"`, le compilateur cherchera le fichier à l'addresse `dir1/subdir/bar.kh`. On peut ajouter un argument `-I` au programme, qui ajouterait un ou plusieurs dossiers à parcourir pour chaque import.


L'instruction class
--------------------

Syntaxe:

`@class ClassName { declarations... }`

Cette instruction crée un espace de nom ClassName; les déclarations dans le bloc class sont traitées de la même façon que dans un bloc module. Le bloc de classe accepte également des déclarations `@member`, qui peuvent définir des variables ou des fonctions membres de ClassName. Lors de la compilation, une structure est créée, dont les champs sont les variables membres de la classe, et un typedef de cette structure est fait vers le nom de la classe. Les fonctions membres sont équivalentes à des fonctions de modules, avec un argument supplémentaire de type ClassName*.

Par défaut, plusieurs fonctions membres sont créées automatiquement (voir Héritage).

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

`@!(type1)[modulename funcname : arg1 : @!(type2)arg2 : ...]` (à vérifier)

`[object funcname : args...]`

`[object.varname]`

Récupère la variable ou exécute la fonction définie dans modulename (modulename peut être une classe). Le type de retour peut être inféré par le compilateur ou précisé par l'utilisateur. Un type ambigu est une erreur de compilation.

Les deux dernières syntaxes sont valides seulement si `object` est un pointeur sur une classe qui possède un membre `funcname`/`varname`. L'avant-dernière syntaxe équivaut à `[ClassName funcname : object : args...]`.

NOTE: Par défaut, les deux dernières syntaxes n'acceptent qu'un nom de variable de type `ClassName *`. Cette approche a l'avantage d'être simple à implémenter, et ne laisser aucune confusion possible. Cependant, elle manque de flexibilité, et oblige le programmeur à déclarer un pointeur pour chaque cas ou l'adresse de `object` est calculée, ce qui ne permet pas des raccourcis simples comme `[&object.varname]`. La solution la plus simple pour ce problème est de rajouter un cas spécial pour `&object`. Une autre solution serait d'autoriser object à être n'importe quelle expression ayant pour type `ClassName *`; cette solution serait plus complexe à implémenter, et créerait des cas ou l'interprétation d'un instruction serait ambiguë. Une autre solution serait de créer une syntaxe spécifique, et non ambiguë, pour la gestion d'une instance d'objet.

TODO - Ajouter new/init/delete/alloc
TODO - Ajouter héritage
