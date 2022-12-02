#Homotéthie

from math import *

def ecart_dist(d_or,d_dest):
    '''Renvoie l'ecart longitude/latitude entre le départ et la destination'''
    if ((float(d_or)*float(d_dest))<0):
        print('1')
        return(d_dest-d_or)
    else:
        return(d_dest-d_or)
    

def rad(x):
    return(x*pi/180)

def get_angle(lon_or, lat_or, lon_dest, lat_dest):
    '''Transforme les donne l'angle correspondant entre le point de départ et le point d'arrivée'''
    delta_lat = ecart_dist(lat_or,lat_dest)
    delta_lon = ecart_dist(lon_or,lon_dest)
    theta = atan(delta_lat/delta_lon)
    return(theta)

def get_dist_km(lon_or, lat_or, lon_dest, lat_dest):
    '''Renvoie la distance en km entre deux points donnés'''
    delta_lat = lat_dest-lat_or
    delta_lon = lon_dest-lon_or
    x=(delta_lon)*cos(0.5*(lat_dest+lat_or))
    y=delta_lat
    dist=sqrt(x**2+y**2)
    dist_km=1.852*60*dist
    return(dist_km)


def get_dist_km_2(lon_or, lat_or, lon_dest, lat_dest):
    a=sin(rad(0.5*(lat_dest-lat_or)))**2+cos(rad(lat_or))*cos(rad(lat_dest))*sin(rad(0.5*(lon_dest-lon_or)))**2
    c=2*atan(sqrt(a)/sqrt(1-a))
    dist=6371*c
    return(dist)

def coord_homotethie(lon_or,lat_or,lon_dest,lat_dest,coef):
    '''renvoie les nouvelles coords selon le coef'''
    dist=get_dist_km_2(lon_or,lat_or,lon_dest,lat_dest)
    angle= rad(get_angle(lon_or,lat_or,lon_dest,lat_dest))
    new_dist = dist*coef
    new_lat=lat_or+(lat_dest-lat_or)*coef
    new_lon=lon_or+(lon_dest-lon_or)*coef
    return(new_lon,new_lat)

