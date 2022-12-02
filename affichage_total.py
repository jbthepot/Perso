import affichage_vol_dest as avd
import affichage_gare_sncf as ags
import calcul_distances as cdist
import folium
import pandas as pd

nom_recherche = 'Angoulême'
def affichage_total(nom_recherche):
    
    
    ####Destinations en avion
    aeroports_recherche = avd.recherche_airport(nom_recherche)
    gares_recherche = ags.recherche_gare(nom_recherche)
    
    nombre_aeroports = aeroports_recherche.shape[0]

    print('Nbr aerpo' +str(nombre_aeroports))

    fmap= folium.Map(location=[45,0])
    couleur =['blue','red','green']
    for i in range(nombre_aeroports):
        
        code_aeroport = aeroports_recherche['code'].iloc[i]
        print('Début aeroport ' + str(i) + ' ' + str(code_aeroport))
        airports_liste = pd.read_csv('Data/ensemble_airports.csv')
        airports_dest=avd.vol_dest_api(code_aeroport)
        
        airport_ori = airports_liste[airports_liste['code']==str(code_aeroport)]
        
        airport_ori_longitude = airport_ori['lon'].iloc[0]
        airport_ori_latitude = airport_ori['lat'].iloc[0]  

        



        folium.Marker([airport_ori_latitude, airport_ori_longitude],
                popup=airport_ori['name'].iloc[0],
                icon=folium.Icon(color='green')).add_to(fmap)

        n = airports_dest.shape[0] #Nombre de gares

        for j in range(n):
            longitude = airports_dest['lon'].iloc[j]
            latitude = airports_dest['lat'].iloc[j]
            nom = airports_dest['cityTo'].iloc[j]
            
            if (not(pd.isna(latitude)) and not(pd.isna(longitude))):
                #Tracé du point
                folium.Marker([latitude, longitude],
                popup=nom ,
                icon=folium.Icon(color='red')).add_to(fmap)
                
                #Tracé de la ligne
                points=[tuple([airport_ori_latitude,airport_ori_longitude]),tuple([latitude,longitude])]
                folium.PolyLine(points, color=str(couleur[i]), weight=2.5, opacity=1).add_to(fmap)
        print('Fin boucle ' + str(i))
        
        
        
    #Destination en train
    
    gares_recherche= ags.requete_destinations_api(nom_recherche)
    
    gares_initiale_latitude = ags.recherche_gare(nom_recherche)['lat'].iloc[0]
    gares_initiale_longitude = ags.recherche_gare(nom_recherche)['lon'].iloc[0]


    departs_gares_latitude =gares_recherche["lat"]
    departs_gares_longitude = gares_recherche["lon"]


    folium.Marker([gares_initiale_latitude, gares_initiale_longitude],
            popup=gares_recherche['label'].iloc[0],
            icon=folium.Icon(color='green')).add_to(fmap)

    n = gares_recherche.shape[0] #Nombre de gares

    for i in range(n):
        longitude = departs_gares_longitude.iloc[i]
        latitude = departs_gares_latitude.iloc[i]
        nom = gares_recherche['label'].iloc[i]
        distance = gares_recherche['Distance'].iloc[i]
        
        if (not(pd.isna(latitude)) and not(pd.isna(longitude))):
            #Tracé du point
            folium.Marker([latitude, longitude],
            popup=nom + ' - ' + str(distance) + ' km',
            icon=folium.Icon(color='blue')).add_to(fmap)
            
            #Tracé de la ligne
            points=[tuple([gares_initiale_latitude,gares_initiale_longitude]),tuple([latitude,longitude])]
            folium.PolyLine(points, color="black", weight=2.5, opacity=1).add_to(fmap)
    
    
    
    
    #Sortie    
    nom_fichier = 'Carte_vol_dest_'+ nom_recherche +'.html'
    fmap.save(outfile='Cartes/' + nom_fichier)
    return(fmap)

affichage_total('Angoulême')