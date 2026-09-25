import folium
import pymongo
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import webbrowser

# ============================================================
# CONFIG - à adapter si besoin
# ============================================================
NOM_BASE = "jardindb"
NOM_COLLECTION = "jardins"   # <-- Vérifie le vrai nom dans Navicat et remplace ici si différent
RAYON_METRES = 10000         # 20 km : les jardins remarquables sont rares, donc rayon large
# ============================================================

# Initialiser le géocodeur (comme dans l'exemple du prof)
geolocator = Nominatim(user_agent="mon_application_jardins")

# Demander l'adresse à l'utilisateur
adresse = input("Entrez une adresse avec la ville ou le code postal: ")

# Géocoder l'adresse
location = geolocator.geocode(adresse)

if location:
    print(f"Latitude : {location.latitude}")
    print(f"Longitude : {location.longitude}")

    # Carte centrée sur l'adresse saisie
    m = folium.Map(location=[location.latitude, location.longitude], tiles=None, zoom_start=10)

    folium.TileLayer(
        tiles=(
            "https://server.arcgisonline.com/ArcGIS/rest/services/"
            "World_Street_Map/MapServer/tile/{z}/{y}/{x}"
        ),
        attr="Tiles © Esri",
        name="Esri World Street Map"
    ).add_to(m)

    # Marqueur du point de départ (adresse saisie)
    street_view_url1 = f"https://www.google.com/maps/@?api=1&map_action=pano&viewpoint={location.latitude},{location.longitude}"
    msg_html1 = f"""
                <div style="font-family: Arial, sans-serif; width: 250px;">
                    <h3 style="color: #4a4a4a; margin-bottom: 10px;">{adresse}</h3>
                    <a href="{street_view_url1}" target="_blank" style="display: inline-block; background-color: #4285F4; color: white; padding: 8px 12px; text-decoration: none; border-radius: 4px; margin-top: 10px;">Voir dans Street View</a>
                </div>
                """
    folium.Marker(
        [location.latitude, location.longitude],
        popup=folium.Popup(msg_html1, max_width=300),
        icon=folium.Icon(color='red', icon='home')
    ).add_to(m)

    # Connexion au serveur MongoDB (comme dans l'exemple du prof)
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient[NOM_BASE]
    mycol = mydb[NOM_COLLECTION]

    Cursor = mycol.find()
    tablo_jardins = list(Cursor)

    nb_affiches = 0

    # Parcours des jardins
    for jardin in tablo_jardins:
        # /!\ Différence avec l'exemple Vélib : ici PAS de sous-clé 'fields',
        # les champs sont directement à la racine du document
        lat = jardin.get("latitude")
        lon = jardin.get("longitude")

        # Certains documents peuvent avoir des coordonnées manquantes -> on les ignore
        if lat is None or lon is None:
            continue

        jardin_location = (lat, lon)
        distance = geodesic((location.latitude, location.longitude), jardin_location).meters

        if distance < RAYON_METRES:
            nom = jardin.get("nom_du_jardin", "Jardin sans nom")
            adresse_jardin = jardin.get("adresse_complete", "Adresse inconnue")
            commune = jardin.get("commune", "")
            annee = jardin.get("annee_obtention", "N/A")
            description = jardin.get("description") or "<p>Pas de description disponible.</p>"

            # sites_internet et telephones_item sont des listes (peuvent être None)
            sites = jardin.get("sites_internet") or []
            site_html = f'<p><a href="{sites[0]}" target="_blank">Site web</a></p>' if sites else ""

            tels = jardin.get("telephones_item") or []
            tel_html = f"<p>Tél : {tels[0]}</p>" if tels else ""

            msg_distance = f"Distance : {int(distance)} m"

            street_view_url = f"https://www.google.com/maps/@?api=1&map_action=pano&viewpoint={lat},{lon}"

            msg_html = f"""
            <div style="font-family: Arial, sans-serif; width: 280px;">
                <h3 style="color: #2e7d32; margin-bottom: 5px;">{nom}</h3>
                <p style="color: #666; margin: 3px 0;">{adresse_jardin}</p>
                <p style="color: #666; margin: 3px 0;">Label obtenu en {annee}</p>
                {tel_html}
                {site_html}
                <p style="color: #666; margin: 3px 0; font-weight: bold;">{msg_distance}</p>
                <a href="{street_view_url}" target="_blank" style="display: inline-block; background-color: #4285F4; color: white; padding: 8px 12px; text-decoration: none; border-radius: 4px; margin-top: 8px;">Voir dans Street View</a>
            </div>
            """

            folium.Marker(
                [lat, lon],
                popup=folium.Popup(msg_html, max_width=320),
                tooltip=nom,
                icon=folium.Icon(color='green', icon='leaf')
            ).add_to(m)

            nb_affiches += 1

    print(f"{nb_affiches} jardin(s) remarquable(s) affiché(s) dans un rayon de {RAYON_METRES} m.")

    # Sauvegarde et ouverture de la carte
    m.save("map_jardins.html")
    print("Carte enregistrée sous map_jardins.html")
    webbrowser.open("map_jardins.html")

else:
    print("Adresse non trouvée.")
