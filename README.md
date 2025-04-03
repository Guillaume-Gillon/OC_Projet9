# OC-Projet9 : Développez une application Web en utilisant Django.

Cette application permet de :<br>
- Demander des critiques de livres ou d’articles en créant un billet <br>
- Lire des critiques de livres ou d’articles <br>
- Publier des critiques de livres ou d’articles <br>
<br>

> [!NOTE]
> Testé sous Ubuntu 24.04 - Python 3.12.3 - Navigateurs Google Chrome et Mozilla Firefox

## Prérequis

Pour installer ce programme, vous aurez besoin d'une connexion internet. Le programme est ensuite exécuté en local et ne nécessite pas de connexion internet pour fonctionner.<br>
<br>
Python doit être installé sur votre ordinateur (version 3.12.3 ou supérieur).<br>
<br>
L'installateur **pip** doit également être disponible sur votre machine pour installer les dépendances.

## Installation et exécution du programme

<details>
<summary>Etape 1 - Installer git</summary><br>

Pour télécharger ce programme, vérifiez que git est bien installé sur votre poste.<br>
Vous pouvez l'installer en suivant les instructions fournies sur le site [git-scm.com](https://git-scm.com/book/fr/v2/D%C3%A9marrage-rapide-Installation-de-Git)

</details>

<details>
<summary>Etape 2 - Cloner le dépôt contenant le programme</summary><br>


Placez-vous dans le dossier souhaité et utilisez la commande suivante :

``git clone https://github.com/Guillaume-Gillon/OC_Projet9.git``

</details>

<details>
<summary>Etape 3 - Créer et activer un evironnement virtuel</summary><br>

Créez un environnement virtuel avec la commande<br>
``python3 -m venv env``<br>

Activez cet environnement avec la commande<br>
``source env/bin/activate``

</details>

<details>
<summary>Etape 4 - Installer les dépendances</summary><br>

Pour que ce programme s'exécute, vous aurez besoin de plusieurs packages additionnels listés dans le fichier requirements.txt.<br>

Exécutez la commande <br>
``pip install -r requirements.txt``

</details>

<details>
<summary>Etape 5 - Lancer un serveur local</summary><br>

Placez vous dans le dossier **litrevu** puis exécutez la commande <br>
``python3 manage.py runserver``

</details>

<details>
<summary>Etape 6 - Ouvrez l'application</summary><br>

Dans la barre d'adresse de votre navigateur, tapez <br>
``http://127.0.0.1:8000/auth/``

</details>

## Fonctionnement du programme

L'application comporte différentes sections :<br>
<br>
- Une page de connexion<br>
- Une page d'inscription<br>
- Une page d'affichage du flux personnalisé<br>
- Une page d'affichage des publications de l'utilisateur<br>
- Une page de gestion des abonnements et des abonnés de l'utilisateur<br>
<br><br>

L'utilisateur a la possibilité de :
- Se connecter / se déconnecter
- Créer une demande de critique
- Créer une critique
- Répondre à une demande de critique
- Modifier ou supprimer ses publications
- S'abonner à des utilisateurs
- Supprimer des abonnements
- Bloquer / Débloquer des utilisateurs
<br><br>

> [!NOTE]
> L'application est fournie avec une base de données contenant les informations suivantes :
> 3 utilisateurs : AdminDatabase - JeanDupont - JulieTellier
> Les mots de passe de ces utilisateurs sont : DefaultPassword
> Seul l'utilisateur AdminDatabase a les droits "superuser"
> Des critiques et des demandes de critiques sont également présents

## Générer un rapport avec flake8-html

Il est possible de générer un rapport avec flake8<br>
Pour ceci, entrez les commandes suivante depuis le répertoire où vous avez installé l'environnement virtuel :<br>

Activer l'environnement virtuel :<br>
``source env/bin/activate``

Lancer la commande pour générer le rapport :<br>
``flake8 litrevu``

Un rapport devrait s'afficher dans votre fenêtre de terminal.<br>
