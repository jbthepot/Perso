# Useful packages
import os
import numpy as np
import pandas as pd
import io
import json
import datetime as pkgdt
import time
import requests 
from requests.adapters import HTTPAdapter
import itertools # list operators
from tqdm import tqdm
import folium
import time
import calcul_distances as cdist

def affichage_vol_api():
    nombre_res =1000
    r=requests.get('https://api.tequila.kiwi.com/locations/box?low_lat=35&low_lon=-13&high_lat=80&high_lon=80&locale=en-US&location_types=airport&limit='+ str(nombre_res) + '&sort=name&active_only=true',headers= {'apikey': 'heKrsP3At973_NDG5Rdo5Hxev6myEuDa', 'accept': 'application/json'})
    
    if r.status_code != 200: # see HTTP errors
        print("HTTP ERROR")
    else:  
        df_tot = []
        r_json =r.json()
        nombre_res = r_json['results_retrieved']
        df = pd.DataFrame(r_json['locations']) # make pandas dataframe from the JSON obtained through the API -- to adapt if format is not JSON
        df['lat'] = 0
        df['lon'] = 0
        for res in range(nombre_res):
            df['lat'].iloc[res] = df['location'].iloc[res]['lat']
            df['lon'].iloc[res] = df['location'].iloc[res]['lon']
        df_tot.append(df)    
        df_fin = pd.concat(df_tot)

        
    return(df_fin)

airports = affichage_vol_api()

airports.to_csv("./Data/ensemble_airports.csv")


#Affichage aeroports

import folium

def affichage_aiport_map():
    '''Affiche les aeroports de la bdd'''
        #Affichage Folium

    
    airports = affichage_vol_api()

    n = airports.shape[0] #Nombre de gares
    
    fmap= folium.Map(location=[airports['lat'].iloc[0],airports['lon'].iloc[0]])
    for i in range(n):
        longitude = airports['lat'].iloc[i]
        latitude = airports['lon'].iloc[i]
        nom = airports['name'].iloc[i]
        
        if (not(pd.isna(latitude)) and not(pd.isna(longitude))):
            #Tracé du point
            folium.Marker([longitude, latitude],
            popup=nom ,
            icon=folium.Icon(color='black')).add_to(fmap)
            
    nom_fichier = 'Carte_airports' +'.html'
    fmap.save(outfile='Cartes/' + nom_fichier)

    print('Finito')
    
    fmap
    return(fmap)
        
affichage_aiport_map()