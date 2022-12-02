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

def vol_dest_api(code):
    nombre_res =1000
    r=requests.get('https://api.tequila.kiwi.com/v2/search?fly_from='+ str(code) +'&dateFrom=29/11/2022&dateTo=30/11/2022',headers= {'apikey': 'heKrsP3At973_NDG5Rdo5Hxev6myEuDa', 'accept': 'application/json'})
    
    if r.status_code != 200: # see HTTP errors
        print("HTTP ERROR")
    else:  
        
        
        
        dest = pd.DataFrame(r.json()['data']) # make pandas dataframe from the JSON obtained through the API -- to adapt if format is not JSON

        airports = pd.read_csv('Data/ensemble_airports.csv')
        dest.rename(columns={'flyTo':'code'}, inplace= True)
        dest_final = pd.merge(dest,airports, on='code', how='left')
        return(dest_final)
    
def recherche_airport(nom_recherche):
    airports = pd.read_csv('Data/ensemble_airports.csv')
    airport_filtre= airports[airports['alternative_names'].str.contains(nom_recherche, na=False)]
    return(airport_filtre)
    
def affichage_vol_dest(code):
           #Affichage Folium
       
    airports = pd.read_csv('Data/ensemble_airports.csv')
    airports_dest=vol_dest_api(code)
    
    airport_ori = airports[airports['code']==str(code)]
    
    airport_ori_longitude = airport_ori['lon'].iloc[0]
    airport_ori_latitude = airport_ori['lat'].iloc[0]  

    


    

    fmap= folium.Map(location=[airport_ori_latitude,airport_ori_longitude])

    folium.Marker([airport_ori_latitude, airport_ori_longitude],
            popup=airport_ori['name'].iloc[0],
            icon=folium.Icon(color='green')).add_to(fmap)

    n = airports_dest.shape[0] #Nombre de gares

    for i in range(n):
        longitude = airports_dest['lon'].iloc[i]
        latitude = airports_dest['lat'].iloc[i]
        nom = airports_dest['cityTo'].iloc[i]
        
        if (not(pd.isna(latitude)) and not(pd.isna(longitude))):
            #Tracé du point
            folium.Marker([latitude, longitude],
            popup=nom ,
            icon=folium.Icon(color='red')).add_to(fmap)
            
            #Tracé de la ligne
            points=[tuple([airport_ori_latitude,airport_ori_longitude]),tuple([latitude,longitude])]
            folium.PolyLine(points, color="red", weight=2.5, opacity=1).add_to(fmap)
    nom_fichier = 'Carte_vol_dest_'+ str(code) +'.html'
    fmap.save(outfile='Cartes/' + nom_fichier)

    print('Finito')
    
    fmap
    return(fmap)
        
#vol_dest_api('BOD')
#affichage_vol_dest('BOD')