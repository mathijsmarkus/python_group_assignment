# Randstad definition
#import geopandas as gpd
import matplotlib.pyplot as plt
import requests
import pandas as pd
import urllib.request, json


stations = pd.read_csv('stations-2023-09.csv')

data = {
    'Station': [] ,
    'Code':[],
    'Lat-coord':[],
    'Lng-coord': [], 
    'Randstad': []
}

df = pd.DataFrame(data)

#Adding the names, codes and coordinates to the dataframe
for i in stations:
    df['Station'] = stations['name_long']
    df['Code'] = stations['code']
    df['Lat-coord'] = stations['geo_lat']
    df['Lng-coord'] = stations['geo_lng']

#Defining the borders of the Randstad
border_n = 52.469165802002 #Long coord of Zaandijk Zaanse Schans
border_o = 5.3705554008484 #Long coord of Amersfoort Central
border_z = 51.790000915527 #Long coord of Dordrecht Zuid

border_z2 = 51.833889007568 #Lat coord of Gorinchem
border_zo2 = 4.9683332443237 #Long coord of Gorinchem
border_o2 = 52.153888702393 #Lat coord of Amersfoort

pointA = [border_z2, border_zo2]
pointB = [border_o2, border_o]

vector1 = [pointB[0] - pointA[0], pointB[1] - pointA[1]]


for i, row in df.iterrows():
    coord1 = row['Lat-coord']
    coord2 = row['Lng-coord']
    
    pointP = [coord1, coord2]
    vector2 = [pointP[0] - pointA[0], pointP[1] - pointA[1]]
    cross_product = vector1[0]*vector2[1] - vector1[1]*vector2[0]


    if coord1 <= border_n and coord1 >= border_z and coord2 <= border_zo2 :
        df.loc[i, 'Randstad'] = 1
    elif coord1 <= border_n and coord1 >= border_z and cross_product <= 0:
        df.loc[i, 'Randstad'] = 1     
    else:
        df.loc[i, 'Randstad'] = 0

df.to_csv('Randstad.csv')
              




