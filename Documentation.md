KOOC

Le KOOC est langage de programmation compilé vers le C. L'exécutable "kooc" prend en paramètre des noms de fichiers .kh et .kc, et crée des fichiers .h et .c en sortie. Par exemple, la commande "kooc foo.kh bar.kc" créera les fichiers "foo.h" et "bar.c".


Les déclarations KOOC

Le langage KOOC est une surcouche du C. Les principaux ajouts du KOOC sont des déclarations, prenant la forme "@nom_de_la_declaration args..." sur une ligne seule, suivie ou non d'un bloc. Sauf précision contraire, ces déclarations se trouvent dans le scope global et ne peuvent pas être inclues dans un bloc, une structure, une fonction, etc.


La déclaration module

La déclaration implement

La déclaration import

La déclaration import prend deux formes:

'@import "filename.kh"'
'@import modulename'

[NOTE: faire une règle pyrser demandant qu'il n'y ait rien d'autre sur la ligne]


Le truc avec le '[]'
