# Dependances
Songfinder utilise :
- `git` : pour le partage de la base de donnee de chants
- `pdflatex` : pour la generation de fichiers PDF

Ces logiciels doivent etre installes pour utiliser ces fonctionalitees.

# Installation
- Depuis un terminal (python doit etre installe) : `pip install songfinder[gui]`
- Depuis l'installeur Windows : [http://devotion-officiel.fr/partage/soft/songFinder/](http://devotion-officiel.fr/partage/soft/songFinder/)

# Recuperer la base de donnees des chants :
La base de donnees est stocke dans un depot git sur bitbucket.
Pour cloner le depot depuis songfinder :
- Aller dans `Editer->Parametres Generaux` et cocher `Synchroniser la base de donnees`.
- Confirmer et remplir les trois champs :
	- Chemin : *https://epef@bitbucket.org/epef/songfinderdata.git*
	- Utilisateur : *[Votre pseudo/prenom]*
	- Mot de passe : *[Me contacter]*
- Cliquer sur `Cloner`.

# Interface graphique
L'interface est organise en trois sections principales :
- Zone de recherche des chants : en haut a gauche
- Zone de gestion des listes de chants : en bas a gauche
- Zone d'edition des chants : a droite

# Interface ligne de commande
Une interface en ligne de commande est disponible se referer a la documentation  : `songfinder --help`

# Editer un chant
- Selectionner le chant voulu dans la zone de recherche
- Utiliser les elements de syntaxes suivants pour controler le decoupage en diapos :
	- `\ss` : Diapo pour un couplet
	- `\sc` : Diapo pour un refrain
	- `\spc` : Diapo pour un pre-refrain
	- `\sb` : Diapo pour un pont
	- `\l` : forcer un saut de ligne
- Un marqueur de diapo qui n'est pas suivi de texte affichera une diapo dont le contenu sera la copie de la derniere diapo appartenant au meme groupe

# Ajouter des accords :

- Selectionner un chant
- Ajouter une ligne debutant par `\ac` et continuant par les accords devant etre affiches.
- Les accords sont associes aux lignes juste au dessus la ligne contenant les accords.
- Les accords peuvent etre renseigne dans la notation francophone ou anglophone.
- Ne remplir les accords que pour un couplet et un refrain, pas besoin de dupliquer chaque serie d'accords.
- Renseigner la tonalite et le nombre de demis ton de transposition (en haut).


# Envoyer les modifications et recuperer celles des autres contributeurs :
- La commande `git` doit etre disponible
- Dans le menu `Reception/Envoi`, cliquer sur `Envoyer les chants` ou `Recevoir les chants`
- Avant des faire des modifications, il faut verifier que quelqu'un d'autre ne les ai pas deja faite en cliquant sur `Recevoir les chants`.
- Apres avoir fait les modifications, il faut envoyer les chants en cliquant sur `Envoyer les chants`.


# Creer un PDF :
- La commande `pdflatex` doit etre disponible
- Faire un double clique sur un chant dans la liste des resultats de recherche (en haut) pour le mettre dans la liste des selections (en bas).
- Repeter cette precedente etape pour tous les chants devant etre dans le PDF
- Dans le menu `PDF` cliquer sur `Generer un fichier PDF`
- Cocher les options de mise en page souhaitees
