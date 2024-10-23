import streamlit as st
import pandas as pd
import numpy as np

st.title('Group project - TIL6022')
st.subheader('Group 6')

st.image('Streamlit_report/report_front_image.jpg')

st.write("**Members**")
st.write("Alene Hooiveld - 5310539   \n Matthijs Markus - 5405416   \n Thijs Daemen - 5289491   \n Niels van der Rijst - 5380162    \n Chris Juárez Overdevest - 5171806")

st.write('Delft, October 25th 2024')

st.header('1. Research objectives')
st.write("""The main research question of this study is:  What are the seat capacities of the train network in the current NS time schedule? 

This question will be answered by answering the following sub-questions: 

- What is the difference in capacities of trains between the Randstad and outside the Randstad? 

- How does the capacity differ between different days of the week? 

- To what extend does the capacity differ when looking at train types, i.e. Sprinter vs. Intercity trains? 
            
- How do other rail transporting companies compare to the NS?""")

st.header('2. Introduction')
st.write("""Every day, more than 1 million passengers use the services of the Dutch national railway company, Nederlandse Spoorwegen (NS). 
         The NS has the concession to run the main rail routes in the Netherlands and operates with 4800 train rides and 260.000 seats per day with Sprinters and Intercity’s. 
         Every year the train schedule is updated and changes are made. Different tracks in the network have different frequencies of train service, which leads to different capacity between cities. 
         To understand and map those differences this project is set up. With databases from the NS an overview is made of the seat capacity between cities on the main rail route. 
         This data is analysed for differences in capacity between cities in- and outside the Randstad, between days of the week and between Sprinters and Intercity’s. 
         """)

st.write("""To make the python script and visualisations in this report the following steps were taken: **@uitleg pythonstrijders**""")

st.header('3. Analysis seat capacity in- and outside the Randstad ')
st.write("""The Netherlands is a small country, but even it has significant regional differences.
         The biggest of this differences can be noticed by looking at the Randstad region. 
         This is the main economic and political hub and of the country and contains most of the big cities. 
         Therefore it is much more developed than other parts of the Netherlands.
         The Randstad is also sometimes counted as one big city conglomeration because of the interconectivity between the cities.
         So, it is expected that the public transport capacity in the Randstad will be significantly higher than in the rest of the country. Seeing figure x, this is the case.""")    
st.write("**insert visual**")

st.write("""In the figure above the stations within the Randstad are displayed with a darker gray color than the non-Randstad stations.
         The Randstad has both a bigger density of stations and all of the red lines(high seat capacity) can be found in the Randstad.
         This can be confirmed by the average amout of trips for the trajectories in the Randstad compared by the tranjectories outside of the Randstad.""")
st.write("""Randstad = 846768,
         Non-Randstad = 262787""")
st.write("""So, the train services in the Randstad have on average more than three times the capacity than their non-Randstad counterparts.
         Next up there will be looked at the trajectories with the highest and lowest capacity.
         These are shown in the tables down below:""") 

df_max = pd.read_csv("Streamlit_report/max_trajectories.csv")  
st.caption("Tabe 1: Trajectories with highest capacity") 
st.table(df_max)

st.caption("Table 2: Trajectories with lowest capacity")
df_min = pd.read_csv("Streamlit_report/min_trajectories.csv")   
st.table(df_min)

st.write("""The trajectories from Table 1 are all situated in the Randstad, while the ones in Table 2 are all outside the randstad.
         This even more accentuates the big differences in these regions""")

st.header('4. Analysis seat capacity for every day of the week ')
st.write("""It is obvious that on some days there is a higher transport demand than on other days. 
         Think for example of the difference between a regular workday and a sunday. 
         So it is expected that the capacity of the railway network would reflect that.
         In the interactive streamlit visual it is possible to look at the capacity for each individual day of the week.""") 
st.write("""**insert visual**""")

st.write("""In the figure it is clear that the capcity does not show significant differences between monday up to friday, 
         but there is a visable difference between the work week and the weekend. 
         To look at these differences in more detail the following graph shows the total capacity for each day of teh week:
         **grafiek beuenen**""")

st.header('5. Analysis seat capacity of Sprinters and InterCity’s ')
st.write("""The NS makes a distinct difference between Sprinters an InterCity trains.
         Sprinter are meant to travel short distances with quick accereration but stop at every small station, 
         while InterCitys are used to transport people between bigger hubs with high speed but skip a lot of smaller stations.
         But what type of train has the higher capacity? In the figure it shows that...""")
st.write("""**insert visual**""")

st.header('6. Interactive map')

# Path to the other .py file
other_file_path = 'map_app_main.py'

# Open and read the content of the external Streamlit file
with open(other_file_path) as f:
    code = f.read()

# Execute the code in the other file
exec(code)

st.header('6. Discussion')

st.header('7. Contribution statement')
