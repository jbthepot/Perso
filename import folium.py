import folium
#Train stations

import pandas as pd
import matplotlib.pyplot as plt



gares = pd.read_csv("train_stations_europe.csv")



code_pays ="FR"
simplifie = True

if simplifie:   
    gares_pays_int = gares
    #gares_pays_int= gares[gares["country"].isin(["FR","ES","DE"])] 
    gares_pays = gares_pays_int[gares_pays_int['is_main_station']==True]
else:
    gares_pays= gares[gares["country"]==code_pays]



gares_pays_latitude =gares_pays["latitude"]
gares_pays_longitude = gares_pays["longitude"]

fmap= folium.Map(location=[gares_pays_latitude.iloc[1],gares_pays_longitude.iloc[1]])


n = gares_pays.shape[0] #Nombre de gares
print(gares_pays_longitude.iloc[2])

for i in range(n):
    longitude = gares_pays_longitude.iloc[i]
    latitude = gares_pays_latitude.iloc[i]
    nom = gares_pays["name"].iloc[i]
    if (not(pd.isna(latitude)) and not(pd.isna(longitude))):
   

        
        folium.Marker([latitude, longitude],
        popup=nom,
        icon=folium.Icon(color='red')).add_to(fmap)
fmap.save('Carte_' + code_pays +".html")
    
    