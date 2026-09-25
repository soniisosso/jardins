Carte des Jardins Remarquables d'Île-de-France

Ce projet génère une carte interactive (map_jardins.html) affichant les jardins labellisés "Jardin remarquable" situés autour d'une adresse donnée par l'utilisateur.

Fonctionnement
L'utilisateur saisit une adresse (ville ou code postal).
Le script géolocalise cette adresse avec geopy (Nominatim/OpenStreetMap).
Il se connecte à une base MongoDB locale contenant les données des jardins remarquables.
Il calcule la distance entre l'adresse saisie et chaque jardin, et n'affiche que ceux situés dans un rayon donné.
Il génère une carte Folium (HTML) avec un marqueur par jardin, et l'ouvre automatiquement dans le navigateur.
Prérequis
Python 3
MongoDB installé et lancé en local (port 27017 par défaut)
Les données du fichier liste-des-jardins-remarquables.json importées dans MongoDB (via Navicat ou mongoimport)
Librairies Python
bash
pip install folium pymongo geopy


Lancer le script
bash
python jardins_remarquables_map.py

Le script demande une adresse dans le terminal, par exemple :

Entrez une adresse avec la ville ou le code postal: 92370
Résultat
Un fichier map_jardins.html est créé dans le dossier du script.
Il s'ouvre automatiquement dans le navigateur par défaut.
Un marqueur rouge indique l'adresse saisie.
Des marqueurs verts (icône feuille) indiquent chaque jardin trouvé dans le rayon défini.
Cliquer sur un marqueur ouvre une popup avec : nom du jardin, adresse, année d'obtention du label, téléphone/site web si disponibles, distance depuis l'adresse saisie, et un lien Street View.
Structure des données (champs utilisés)
Champ MongoDB	Description
nom_du_jardin	Nom du jardin
adresse_complete	Adresse postale
commune	Commune (en majuscules, sans accent)
departement	Nom du département
code_departement	Numéro du département
latitude / longitude	Coordonnées GPS
annee_obtention	Année d'obtention du label (texte)
types_item	Liste des types du jardin
sites_internet	Liste de liens (peut être vide)
telephones_item	Liste de téléphones (peut être vide)
