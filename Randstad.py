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
border_s = 51.790000915527 #Long coord of Dordrecht Zuid

lat1 = 51.833889007568 #Lat coord of Gorinchem
long1 = 4.9683332443237 #Long coord of Gorinchem
lat2 = 52.153888702393 #Lat coord of Amersfoort Centraal
long2 = 5.3705554008484 #Long coord of Amersfoort Centraal

pointA = [lat1, long1]
pointB = [lat2, long2]

vector1 = [pointB[0] - pointA[0], pointB[1] - pointA[1]] #Line between Gorinchem and Amersfoort Centraal 


for i, row in df.iterrows():
    coord1 = row['Lat-coord'] #Lat coord of station i
    coord2 = row['Lng-coord'] #Long coord of station i
    
    pointP = [coord1, coord2] #Vector of station i
    vector2 = [pointP[0] - pointA[0], pointP[1] - pointA[1]] 
    cross_product = vector1[0]*vector2[1] - vector1[1]*vector2[0] 


    if coord1 <= border_n and coord1 >= border_s and coord2 <= long1 : #Checks for north of Dordrecht-Zuid, south of Zaandijk Zaanse Schans and west of Gorinchem
        df.loc[i, 'Randstad'] = 1
    elif coord1 <= border_n and coord1 >= border_s and cross_product <= 0: #Checks for north of Dordrecht-Zuid, south of Zaandijk Zaanse Schans and west of the line between Gorinchem and Amersfoort Centraal
        df.loc[i, 'Randstad'] = 1     
    else:
        df.loc[i, 'Randstad'] = 0

df.to_csv('Randstad.csv')
              




