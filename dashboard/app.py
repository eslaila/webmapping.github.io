import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import folium_static
import pandas as pd
from branca.colormap import LinearColormap
import numpy as np
# Charger les données géospatiales depuis le fichier GeoParquet
path_to_geoparquet = "donnees\geoparquet\OUTPUT1500.geoparquet"
gdf = gpd.read_parquet(path_to_geoparquet)

st.set_page_config(
    page_title="visualisation",
    page_icon="🌍",
    layout="wide",  
)

# Titre de l'application
st.markdown("<h2 style='font-size:32px;text-align:center;'>Visualisation des données </h2>", unsafe_allow_html=True)


# Sidebar pour la sélection de l'option (Attribut/Propriété)
option = st.sidebar.radio("Choisir une option", ("Attribut", "Propriété"))

if option == "Attribut":
    # Liste des attributs pour le choix
    attributs = ['temperature', 'pression_atmosph', 'pluviometrie']
    selected_attribute = st.sidebar.selectbox("Sélectionner un attribut", attributs)

    # Liste des jours pour le choix
    jours = [6, 5, 4, 3, 2, 1, 0]
    selected_day = st.sidebar.selectbox("Sélectionner un jour", jours)

    # Filtrer les données en fonction de l'attribut et du jour sélectionnés
    selected_column_day = f'{selected_attribute}jour{selected_day}'
    filtered_data = gdf[gdf[selected_column_day] >= 0]

    # Classer les valeurs en utilisant la méthode de Jenks
    
    bins = np.linspace(filtered_data[selected_column_day].min(), filtered_data[selected_column_day].max(), num=6)
    # Créer une carte Folium centrée sur la moyenne des coordonnées des géométries
    m = folium.Map(location=[gdf['geometry'].centroid.y.mean(), gdf['geometry'].centroid.x.mean()], zoom_start=4)


    # Ajouter les données à la carte en tant que symboles proportionnels
    for idx, row in filtered_data.iterrows():
        popup = f"{selected_column_day}: {row[selected_column_day]}"
        
        # Assigner une couleur en fonction de la classe Jenks
        color = '#f1eef6' if row[selected_column_day] <= bins[1] else \
                '#bdc9e1' if row[selected_column_day] <=bins[2] else \
                '#74a9cf' if row[selected_column_day] <=bins[3] else \
                '#2b8cbe' if row[selected_column_day] <=bins[4] else \
                '#045a8d'  

        folium.CircleMarker(
            location=[row['geometry'].y, row['geometry'].x],
            radius= 5,  # Ajuster l'échelle pour la taille des symboles
            popup=popup,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.6,
        ).add_to(m)

else:
    # Liste des propriétés pour le choix
    proprietes = [ 'humidité', 'Reflectance']
    selected_property = st.sidebar.selectbox("Sélectionner une propriété", proprietes)
    min,max=0,1
    # Classer les valeurs en utilisant la méthode de Jenks
    bins = np.linspace(gdf[selected_property].min(), gdf[selected_property].max(), num=6)

    # Créer une carte Folium centrée sur la moyenne des coordonnées des géométries
    m = folium.Map(location=[gdf['geometry'].centroid.y.mean(), gdf['geometry'].centroid.x.mean()], zoom_start=4)

      # Définir les couleurs pour les classes
    colors = ['#f1eef6', '#bdc9e1', '#74a9cf', '#2b8cbe', '#045a8d']

    # Ajouter les données à la carte avec des couleurs pour les classes
    for idx, row in gdf.iterrows():
        popup = f"{selected_property}: {row[selected_property]}"
        
        # Assigner une couleur en fonction de la classe Jenks
        color = '#f1eef6' if row[selected_property] <= bins[1] else \
                '#bdc9e1' if row[selected_property] <=  bins[2] else \
                '#74a9cf' if row[selected_property] <=  bins[3] else \
                '#2b8cbe' if row[selected_property] <=  bins[4] else \
                '#045a8d'
       
        value = row[selected_property]

        folium.CircleMarker(
            location=[row['geometry'].y, row['geometry'].x],
            radius=5,
            popup=popup,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.6,
        ).add_to(m)

colors=['#f1eef6','#bdc9e1','#74a9cf','#2b8cbe','#045a8d']    
cmap = LinearColormap(colors=colors, vmin = round(bins.min(), 2),vmax = round(bins.max(), 2))
cmap.caption = ' Légende'
cmap.add_to(m)
    # Afficher la carte dans Streamlit
folium_static(m ,width=800, height=600)
