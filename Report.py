import streamlit as st
import pandas as pd
import numpy as np
from Streamlit_report import statistics_report


st.title('Group project - TIL6022')
st.subheader('Group 6')


st.image('Streamlit_report/report_front_image.jpg')


st.write("**Members**")
st.write("Alene Hooiveld - 5310539   \n Matthijs Markus - 5405416   \n Thijs Daemen - 5289491   \n Niels van der Rijst - 5380162    \n Chris Juárez Overdevest - 5171806")

st.write('Delft, November 5th 2024')

st.header('1. Research objectives')

st.write("""The main research question of this study is:  What are the seat capacities of the train network in the current NS, Arriva, Keolis and Qbuzz time schedule? 

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

st.write(""""The results are visualised in a interactive map (chapter 6), this is the main delivearble of this project and all sub-questions are answered by using this map""")
st.markdown("[Go to 6. Interactive Map](#6-interactive-map)")

st.header('3. Analysis seat capacity in- and outside the Randstad ')
st.write("""The Netherlands is a small country, but even it has significant regional differences.
         The biggest of this differences can be noticed by looking at the Randstad region. 
         This is the main economic and political hub and of the country and contains most of the big cities. 
         Therefore it is much more developed than other parts of the Netherlands.
         The Randstad is also sometimes counted as one big city conglomeration because of the interconectivity between the cities.
         So, it is expected that the public transport capacity in the Randstad will be significantly higher than in the rest of the country. 
         Looking at the interactive map in chapter 6, this is the case.""")    

st.write("""In the interactive map, the stations within the Randstad are displayed with a darker gray color than the non-Randstad stations.
         The Randstad has both a bigger density of stations and all of the red lines(high seat capacity) can be found in the Randstad.
         This can be confirmed by the average amout of trips for the trajectories in the Randstad compared by the tranjectories outside of the Randstad.""")
st.write("""Randstad = 846768,
         Non-Randstad = 262787""")
st.write("""So, the train services in the Randstad have on average more than three times the capacity than their non-Randstad counterparts.
         Next up there will be looked at the trajectories with the highest and lowest capacity.
         These are shown in the tables down below:""") 

df_max = pd.read_csv("Streamlit_report/max_trajectories.csv")  
st.caption("Tabe 1: Trajectories with highest capacity") 
st.dataframe(df_max, use_container_width=True, hide_index=True)

st.caption("Table 2: Trajectories with lowest capacity")
df_min = pd.read_csv("Streamlit_report/min_trajectories.csv")   
st.dataframe(df_min, use_container_width=True, hide_index=True)

st.write("""The trajectories from Table 1 are all situated in the Randstad, while the ones in Table 2 are all outside the randstad.
         This even more accentuates the big differences in these regions""")

st.header('4. Analysis seat capacity for every day of the week ')
st.write("""It is obvious that on some days there is a higher transport demand than on other days. 
         Think for example of the difference between a regular workday and a sunday. 
         So it is expected that the capacity of the railway network would reflect that.
         In the interactive streamlit visual it is possible to look at the capacity for each individual day of the week.""") 
st.markdown("[Go to 6. Interactive Map](#6-interactive-map)")


st.write("""In the figure it is clear that the capcity does not show significant differences between Monday up to Friday, 
         but there is a visable difference between the work week and the weekend. In the map that shows the Monday to Friday, the tracks
         more red colored than during the weekend.
         To look at these differences in more detail the following graph shows the total capacity for each day of the week:
         """)

st.image('Streamlit_report/mooie graph.png')
st.caption("Figure 1: Variation of the total seat capacity during the week") 

st.write("""Another interesting statistic is the difference in maximum and minimum seat capacity per route during the week. 
         This indicates to what extent the train schedule varies throughout the week. Table 3 presents the ten largest differences. 
         Seat capacity in Randstad's major cities varies significantly throughout the week.""")

st.caption('Table 3: The trajects with the highest difference between the minimum and maximum seat capacity in a week')
df_difference = pd.read_csv("Streamlit_report/Max difference capacity.csv")
st.dataframe(df_difference.head(10), use_container_width=True, hide_index=True)


st.header('5. Analysis seat capacity of Sprinters and InterCity’s ')
st.write("""The NS makes a distinct difference between Sprinters an InterCity trains.
         Sprinter are meant to travel short distances with quick accereration but stop at every small station, 
         while InterCitys are used to transport people between bigger hubs with high speed but skip a lot of smaller stations.
         But what type of train has the higher capacity? """)
st.markdown("[Go to 6. Interactive Map](#6-interactive-map)")

st.write('''In the interactive map the capacities for either sprinters and intercity's can be selected. However,
         precise differences are not visible. In figure 2 the seat capacities per day for all sprinters and intercity's are presented.
         The figure shows clearly that the seat capacity of all the intercity's is significantly higher than the seat capacity 
         of all the sprinters. ''')

st.image('Streamlit_report/nog een mooie graph.png')
st.caption("Figure 2: Difference in capacity between intercity's and sprinters") 

st.write('''This result is supported by the week total and average of both the sprinters and intercity's, which is presented in table 4.''')
st.caption("Table 4: Week total and average for sprinters and intercity's")
df = statistics_report.traintypes_avg_total()
st.dataframe(df, use_container_width=True, hide_index=True)


st.markdown("## 6. Interactive Map")

# Path to the other .py file
other_file_path = 'Streamlit_report/map_app_main.py'

# Open and read the content of the external Streamlit file
with open(other_file_path) as f:
    code = f.read()

# Execute the code in the other file
exec(code)

st.header('7. Discussion')

st.write('''In this project the following main question is researched:''') 
st.write('''*What are the seat capacities of the train network in the current NS time schedule?* ''')
st.markdown('''This question was studied by gathering and analyzing data from the NS, Keolis, Qbuzz and Arriva and creating an interactive map of all seat capacities. 
            With this data and the map the subquestions were answered. \n In conclusion, seat capacities are higher for Randstad stations than for non-Randstad stations, higher for week days than for weekend days and higher for intercity's than for sprinters.
            This is in line with what was expected before the study was performed.
         
        
            RNET tussen alphen en gouda is van NS maar staat niet in de database ''')

st.header('8. Contribution statement')

