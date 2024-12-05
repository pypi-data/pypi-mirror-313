# Librairie Python MSICPE

Le dépôt de la librairie msicpe ainsi que les documentations associées sont disponibles ici :

- Dépôt : <https://gitlab.in2p3.fr/cpe/msi/toolbox> 
- Doc : <https://cpe.pages.in2p3.fr/msi/toolbox>

Table des matières

> [Introduction](#_Toc183686718)<br/>
> [Créer un nouveau module dans une librairie](#_Toc183686719)<br/>
> [Ajouter/Mettre à jour une fonction existante dans un module](#_Toc183686720)<br/>
>> [Déposer le code et générer une version de test disponible sur test.pypi.org](#_Toc183686721)<br/>
>> [Déposer le code et générer une version de disponible sur pypi.org](#_Toc183686722)<br/>
>> [Déposer le code sans vouloir générer de version de la librairie](#_Toc183686723)<br/>

## Introduction

Certains outils d’intégration continue ont été installé sur le dépôt gitlab de chacune des librairies pour faciliter la génération de la documentation technique ainsi que la compilation de la librairie et son dépôt sur pypi.org ou test.pypi.org. Cependant, cela requiert quelques actions de votre part qui sont détaillées dans la suite du document.

## Créer un nouveau module dans une librairie
Dans le dépôt git, vous trouverez l’arborescence suivante :<br/>
<img src="docs/images/arborescence.png"
     alt="Arborescence Structure"
     style="float: left; margin-right: 10px;" />
1. [ ] Créez un nouveau dossier dans le dossier « src/nom de la libraire/_nom du module »_ (dans l’exemple ci-dessous le nouveau dossier se trouverait au même niveau que ssl, tns, tsa ou utils…)
2. [ ] Pour que le contenu de ce nouveau dossier soit reconnu comme un nouveau module de la librairie, il est nécessaire que ce dossier contienne un fichier **\__init_\_.py** qui va lister le lien vers toutes les fonctions du module.
3. [ ] Si vous souhaitez que la documentation de ce module soit automatiquement générée :
    1. Copier le fichier « docs/msicpe.tns.rst » et renommez le « msicpe._nom du module._rst ».
    2. Adapter le contenu du fichier.
    3. Editez le fichier « docs/msicpe.rst » en ajoutant « msicpe._nom du module »_ à la suite de la liste déjà existante dans ce fichier.
4. Continuer en suivant les instructions de la partie suivante

## Ajouter/Mettre à jour une fonction existante dans un module

Dans le dossier du module où vous souhaitez ajouter la fonction _myFunc_ :
1. [ ] Créer un fichier _maFonction.py_ qui contiendra :
	1. Les imports nécessaires pour l’exécution des fonctions de ce fichier
	2. Une (ou plusieurs) fonction(s) python _myFunc_ (..)
	3. La doc string descriptive de la fonction qui respecte la nomenclature suivante
````			
def sptheo(Q, method, fenetre=None):
	"""
	Calcule dans le cadre du TP Estimation spectrale :

	- Gth : la valeur en dB de la DSPM du bruit blanc filtré entre 0 et 0,5.
	- Gbiais : la valeur en dB de Gth convolué par la grandeur régissant le biais attaché à la 'method'.
	- f : un vecteur fréquence réduite de même taille que Gth et Gbiais.

	Parameters
	----------
	Q : int
		Pour 'simple', représente la longueur de l'échantillon analysé.
		Pour 'moyenne' ou 'welch', représente la longueur d'une tranche.

	method : {'simple', 'moyenne', 'welch'}
		Méthode d'estimation spectrale à utiliser.

	fenetre : str, optional
		Nom de la fenêtre à utiliser si method='welch'. Ignoré pour 'simple' et 'moyenne'.

	Returns
	-------
	Gth : ndarray
		Valeur en dB de la DSPM du bruit blanc filtré entre 0 et 0,5.

	Gbiais : ndarray
		Valeur en dB de Gth convolué par la grandeur régissant le biais.

	f : ndarray
		Vecteur fréquence réduite.

	Notes
	-----
	Cette fonction calcule différentes valeurs théoriques dans le cadre de l'estimation spectrale,
	en fonction de la méthode choisie ('simple', 'moyenne' ou 'welch') et des paramètres associés.

	Example
	-------
	>>> from msicpe.tsa import sptheo
	>>> sptheo(1024, 'welch', 'hamming')
	"""

````


2. [ ]  Editer le fichier **\__init_\_.py** du même dossier pour importer la fonction qui doit être accessible dans la librairie.


<i>Par exemple, si je veux que la fonction export_dat disponible dans le fichier export_dat.py soit accessible, je vais compléter le fichier_ **\__init_\_.py** de la façon suivante :</i>

```
from .export_dat import export_dat
```

3. [ ] Il faut maintenant déposer le code sur le dépôt git. Trois options s’offrent à vous :  
    \- Déposer le code et générer une version de test disponible sur test.pypi.org<br/>
	\- Déposer le code et générer une version de disponible sur pypi.org<br/>
	\- Déposer le code sans vouloir générer de version de la librairie

### Déposer le code et générer une version de test disponible sur test.pypi.org

- [ ] Modifier le fichier **version.txt** situé à la racine du dépôt et indiquer une suite de chiffre supérieure à celle disponible sur <https://test.pypi.org/simple/msicpe/>
- [ ] Faites un simple commit & push
- [ ] La doc sera mise à jour et d’ici quelques minutes (~5 min) il y aura une nouvelle version de la librairie qui sera disponible sur <https://test.pypi.org/simple/msicpe/>

### Déposer le code et générer une version de disponible sur pypi.org

- [ ] Faites un simple commit & push
- [ ] Sur le repo, créer un tag de la dernière version du git (en suivant la numérotation croissante existante).
- [ ] La doc sera mise à jour et d’ici quelques minutes (~5 min) il y aura une nouvelle version de la librairie qui sera disponible sur <https://pypi.org/project/msicpe/>

### Déposer le code sans vouloir générer de version de la librairie

- [ ] Faites un simple commit & push