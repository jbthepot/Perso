#Train stations
import folium
import pandas as pd
import matplotlib.pyplot as plt

gares = pd.read_csv("train_stations_europe.csv")

#Gares de France

def affichage_gares_france():
    gares_france= gares[gares["country"]=='FR']

    gares_france_latitude =gares_france["latitude"]
    gares_france_longitude = gares_france["longitude"]

    plt.scatter(gares_france_longitude,gares_france_latitude, color="red")
    plt.show()
    return()

#Gares de UK


def affichage_gares_europe():
    
    gares_latitude =gares["latitude"]
    gares_longitude = gares["longitude"]

    plt.scatter(gares_longitude,gares_latitude, color="green")
    plt.title("Emplacements des gares en Europe")
    plt.xlabel("Longitude (°)")
    plt.ylabel("Latitude (°)")
    plt.grid()
    plt.show()
    return()


def affichage_gares_pays(code_pays):
    "Affiche les gares du pays souhaité. Pour l'Europe, entre le code pays EU"
    if code_pays in ("EU","UE"):
        
        affichage_gares_europe()
    
    else:

        gares_pays = gares[gares["country"] == code_pays]

        gares_pays_latitude = gares_pays["latitude"]
        gares_pays_longitude = gares_pays["longitude"]

        plt.scatter(gares_pays_longitude, gares_pays_latitude, color="orange")
        plt.title("Emplacement des gares du pays " + code_pays)
        plt.xlabel("Longitude (°)")
        plt.ylabel("Latitude (°)")
        plt.grid()
        plt.show()
        plt.show()
        folium.Map(gares_pays_longitude,gares_pays_longitude)
    return()

#Affichage des gares d'un pays particulier

code_pays="DK" #France =FR, Allemagne = DE, grande Bretagne = GB, etc.

affichage_gares_pays(code_pays)
