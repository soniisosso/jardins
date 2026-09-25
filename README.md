# 🌿 Carte des Jardins Remarquables d'Île-de-France
 
Application Python générant une carte interactive permettant de localiser les jardins labellisés **"Jardin remarquable"** en Île-de-France, à partir d'une adresse saisie par l'utilisateur.
 
---
 
## 📋 Sommaire
 
- [Technologies utilisées](#-technologies-utilisées)
- [Fonctionnalités](#-fonctionnalités)
- [Architecture du projet](#-architecture-du-projet)
- [Fonctionnement détaillé](#-fonctionnement-détaillé)
- [Prérequis](#-prérequis)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [Structure des données](#-structure-des-données)
- [Captures d'écran](#-captures-décran)
- [Personnalisation](#-personnalisation)
- [Dépannage](#-dépannage)
---
 
## 🛠 Technologies utilisées
 
| Technologie | Rôle |
|---|---|
| **Python 3** | Langage principal de l'application |
| **MongoDB** | Base de données NoSQL stockant les jardins remarquables (import du jeu de données open data) |
| **PyMongo** | Driver Python pour interroger MongoDB |
| **Geopy (Nominatim)** | Géocodage : conversion d'une adresse / code postal en coordonnées GPS (latitude/longitude), via l'API OpenStreetMap |
| **Folium** | Génération de cartes interactives (basées sur Leaflet.js) exportées en HTML |
| **Esri World Street Map** | Fond de carte (tuiles) affiché dans le navigateur |
| **Navicat** | Outil utilisé pour l'administration de la base MongoDB et l'import du dataset JSON |
| **Google Street View** | Intégration d'un lien direct vers la vue à 360° de chaque jardin |
 
**Source des données** : jeu de données open data "Liste des jardins remarquables" (Île-de-France).
 
---
 
## ✨ Fonctionnalités
 
- Saisie d'une adresse ou d'un code postal par l'utilisateur
- Géolocalisation automatique de cette adresse
- Recherche des jardins remarquables situés dans un rayon donné autour de cette adresse
- Affichage sur une carte interactive avec :
  - un marqueur pour l'adresse recherchée
  - un marqueur par jardin trouvé, avec popup détaillée (nom, adresse, année d'obtention du label, contact, distance)
  - un lien direct vers Google Street View pour chaque point
- Export automatique de la carte en fichier HTML, ouvert dans le navigateur par défaut
---
 
## 🏗 Architecture du projet
 
```
├── jardins_remarquables_map.py   # Script principal
├── map_jardins.html              # Carte générée (créée à l'exécution)
└── README.md                     # Ce fichier
```
 
**Base de données MongoDB**
 
```
jardindb (base)
└── jardins (collection)   # documents importés depuis le JSON open data
```
 
---
 
## ⚙️ Fonctionnement détaillé
 
Le script suit un pipeline en 4 étapes :
 
### 1. Géocodage de l'adresse
```python
geolocator = Nominatim(user_agent="mon_application_jardins")
location = geolocator.geocode(adresse)
```
L'adresse saisie (ville, code postal...) est transformée en coordonnées GPS via l'API Nominatim.
 
### 2. Initialisation de la carte
```python
m = folium.Map(location=[location.latitude, location.longitude], tiles=None, zoom_start=10)
```
Une carte Folium est centrée sur l'adresse trouvée, avec un fond de carte Esri.
 
### 3. Requête MongoDB et filtrage géographique
```python
mycol = mydb[NOM_COLLECTION]
tablo_jardins = list(mycol.find())
```
Tous les jardins sont récupérés depuis MongoDB, puis pour chacun on calcule la distance à vol d'oiseau avec `geopy.distance.geodesic` entre l'adresse saisie et le jardin. Seuls les jardins à moins de `RAYON_METRES` sont conservés.
 
### 4. Génération des marqueurs et export
Pour chaque jardin retenu, une popup HTML est construite dynamiquement (nom, adresse, année d'obtention, contact, distance, lien Street View), puis ajoutée à la carte. La carte finale est sauvegardée en HTML et ouverte automatiquement dans le navigateur.
 
---
 
## 📦 Prérequis
 
- Python 3.8 ou supérieur
- MongoDB installé et démarré en local (port `27017`)
- Le jeu de données `liste-des-jardins-remarquables.json` importé dans MongoDB
---
 
## 🚀 Installation
 
1. **Installer les dépendances Python**
```bash
pip install folium pymongo geopy
```
 
2. **Importer les données dans MongoDB** (via Navicat ou `mongoimport`)
```bash
mongoimport --db jardindb --collection jardins --file liste-des-jardins-remarquables.json --jsonArray
```
 
3. **Vérifier le nom de la base et de la collection** dans le script :
```python
NOM_BASE = "jardindb"
NOM_COLLECTION = "jardins"
RAYON_METRES = 20000
```
 
---
 
## ▶️ Utilisation
 
```bash
python jardins_remarquables_map.py
```
 
Le programme demande une adresse dans le terminal :
```
Entrez une adresse avec la ville ou le code postal: 92370
```
 
Il affiche ensuite les coordonnées trouvées, le nombre de jardins détectés, puis ouvre automatiquement la carte dans le navigateur.
 
---
 
## 🗂 Structure des données
 
| Champ MongoDB | Description |
|---|---|
| `nom_du_jardin` | Nom du jardin |
| `adresse_complete` | Adresse postale complète |
| `commune` | Commune (majuscules, sans accent) |
| `departement` | Nom du département |
| `code_departement` | Numéro du département |
| `latitude` / `longitude` | Coordonnées GPS |
| `annee_obtention` | Année d'obtention du label (texte) |
| `types_item` | Liste des types de jardin (Public, Parc paysager...) |
| `sites_internet` | Liste de liens (peut être vide) |
| `telephones_item` | Liste de téléphones (peut être vide) |
 
---
 
## 📸 Captures d'écran
 
 
### Saisie du code postal / de l'adresse
<img width="367" height="58" alt="image" src="https://github.com/user-attachments/assets/44d339c0-b195-434e-9eb3-70463dae24e6" />

 
### Carte générée avec les jardins trouvés
<img width="957" height="441" alt="image" src="https://github.com/user-attachments/assets/8d6c101b-b57c-4d0d-9886-8ea1bf96e99c" />


 
### Détail d'une popup jardin
<img width="959" height="473" alt="image" src="https://github.com/user-attachments/assets/95622ff4-68b1-4c61-8df4-f069e275d9ca" />
<img width="959" height="440" alt="image" src="https://github.com/user-attachments/assets/0c486aa9-1f54-4cc3-8ad6-7e9d0c66c31c" />

 
---
 
## 🎛 Personnalisation
 
- **Modifier le rayon de recherche** : ajuster `RAYON_METRES` dans le script.
- **Afficher tous les jardins sans filtre de distance** : supprimer la condition de distance et sortir le bloc d'affichage de la boucle conditionnelle.
- **Enrichir les popups** : ajouter d'autres champs disponibles via `jardin.get("nom_du_champ")`.
---
 
## 🔧 Notes
Problèmes de sites web dans les données, parfois ca ne s'affichera pas.
