declaration Import
{
	pour les fichiers :
	     vérifier que le fichier n'a pas déjà été inclus dans le fichier courant.
	     intégrer la raw '#include "<filename>"' dans la declaration de l'AST du fichier courant.
	     lancer un nouveau parsing du fichier inclue.
	     intégrer les Raw "#ifndef" "# define" "#endif" dans l'ast du fichier.
	     ajouter le fichier à la liste des fichers inclus.

	pour les modules :
	     vérifier que le module n'est pas déjà importé

}

declaration module
{

}