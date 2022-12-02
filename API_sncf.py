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

def page_gares(numero_page) :
    return requests.get(
        ('https://api.sncf.com/v1/coverage/sncf/stop_areas?start_page={}').format(numero_page),
        auth=('16cbfb01-1943-471f-aac9-7a1139abab77', ''))

######################################
# on commence par la première page qui nous donne le nombre de résultats par page ainsi que le nombre total de résultats

page_initiale = page_gares(0)
item_per_page = page_initiale.json()['pagination']['items_per_page']
total_items = page_initiale.json()['pagination']['total_result']
dfs = []

# on fait une boucle sur toutes les pages suivantes
print_done = {}

for page in range(int(total_items/item_per_page)+1) :
    stations_page = page_gares(page)

    ensemble_stations = stations_page.json()

    if 'stop_areas' not in ensemble_stations:
        # pas d'arrêt
        continue

    # on ne retient que les informations qui nous intéressent
    for station in ensemble_stations['stop_areas']:

        station['lat'] = station['coord']['lat']
        station["lon"]  = station['coord']['lon']

        if 'administrative_regions' in station.keys() :
            for var_api, var_df in zip(['insee','name','label','id','zip_code'],
                                       ['insee','region','label_region','id_region','zip_code']):
                try:
                    station[var_df] = station['administrative_regions'][0][var_api]
                except KeyError:
                    if var_api not in print_done:
                        print("key '{0}' not here but {1}".format(var_api,
                                ",".join(station['administrative_regions'][0].keys())))
                        print_done[var_api] = var_api

        [station.pop(k,None) for k in ['coord','links','administrative_regions', 'type', 'codes']]

    stations = ensemble_stations['stop_areas']
    try:
        dp = pd.DataFrame(stations)
    except Exception as e:
        # La SNCF modifie parfois le schéma de ses données.
        # On affiche station pour avoir une meilleure idée que l'erreur retournée par pandas
        raise Exception("Problème de données\n{0}".format(stations)) from e

    dfs.append(dp)
    if page % 10 == 0:
        print("je suis à la page", page, "---", dp.shape)

import pandas
df = pandas.concat(dfs)
df.to_csv("./ensemble_gares.csv")
print(df.shape)
df.head()