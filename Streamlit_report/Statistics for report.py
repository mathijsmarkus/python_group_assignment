import pandas as pd
import matplotlib.pyplot as plt

'''In this file the statistics used in the report are generated'''

#Importing the data files
randstad = "Randstad-0.0.csv"
week_trajectory = 'OutputData/PlotDataWeekall.csv' 
randstad = "Randstad-0.0.csv"
week_trajectory = 'PlotDataWeekall.csv' 
stations = pd.read_csv('../python_group_assignment/stations-2023-09.csv')

monday = pd.read_csv('OutputData/PlotData2024-10-07all.csv', index_col='Unnamed: 0')
tuesday = pd.read_csv('OutputData/PlotData2024-10-08all.csv', index_col='Unnamed: 0')
wednesday = pd.read_csv('OutputData/PlotData2024-10-09all.csv', index_col='Unnamed: 0')
thursday = pd.read_csv('OutputData/PlotData2024-10-10all.csv', index_col='Unnamed: 0')
friday = pd.read_csv('OutputData/PlotData2024-10-11all.csv', index_col='Unnamed: 0')
saturday = pd.read_csv('OutputData/PlotData2024-10-12all.csv', index_col='Unnamed: 0')
sunday = pd.read_csv('OutputData/PlotData2024-10-13all.csv', index_col='Unnamed: 0')

monday_sprinter = pd.read_csv('OutputData/PlotData2024-10-07sprinters.csv', index_col='Unnamed: 0')
tuesday_sprinter = pd.read_csv('OutputData/PlotData2024-10-08sprinters.csv', index_col='Unnamed: 0')
wednesday_sprinter = pd.read_csv('OutputData/PlotData2024-10-09sprinters.csv', index_col='Unnamed: 0')
thursday_sprinter = pd.read_csv('OutputData/PlotData2024-10-10sprinters.csv', index_col='Unnamed: 0')
friday_sprinter = pd.read_csv('OutputData/PlotData2024-10-11sprinters.csv', index_col='Unnamed: 0')
saturday_sprinter = pd.read_csv('OutputData/PlotData2024-10-12sprinters.csv', index_col='Unnamed: 0')
sunday_sprinter = pd.read_csv('OutputData/PlotData2024-10-13sprinters.csv', index_col='Unnamed: 0')

monday_intercity = pd.read_csv('OutputData/PlotData2024-10-07intercities.csv', index_col='Unnamed: 0')
tuesday_intercity = pd.read_csv('OutputData/PlotData2024-10-08intercities.csv', index_col='Unnamed: 0')
wednesday_intercity = pd.read_csv('OutputData/PlotData2024-10-09intercities.csv', index_col='Unnamed: 0')
thursday_intercity = pd.read_csv('OutputData/PlotData2024-10-10intercities.csv', index_col='Unnamed: 0')
friday_intercity = pd.read_csv('OutputData/PlotData2024-10-11intercities.csv', index_col='Unnamed: 0')
saturday_intercity = pd.read_csv('OutputData/PlotData2024-10-12intercities.csv', index_col='Unnamed: 0')
sunday_intercity = pd.read_csv('OutputData/PlotData2024-10-13intercities.csv', index_col='Unnamed: 0')

intercities = pd.read_csv('OutputData/PlotDataWeekintercities.csv', index_col='Unnamed: 0')
sprinters = pd.read_csv('OutputData/PlotDataWeeksprinters.csv', index_col='Unnamed: 0')

#List of the trajects with the overall minimum and maximum seat capacity.
def min_max_week():
    df = pd.read_csv(week_trajectory, index_col =  'Unnamed: 0')
    sorted_df= df.sort_values(by = 'Seats', ascending=False)
    print(sorted_df.head(10))
    print(sorted_df.tail(10)) 

#Plot of the total seats vs the day of the week
def graph_differences():
    total_days = []
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    data = [monday, tuesday, wednesday, thursday, friday, saturday, sunday]
    for i in data:
        total_seats = i['Seats'].sum()
        total_days.append(total_seats)
    
    plt.figure(figsize=(10, 6))
    plt.plot(days, total_days, marker='o', linestyle='-', color='skyblue', linewidth=2, markersize=8)
    plt.title('Total Seats per Day')
    plt.xlabel('Days of the Week')
    plt.ylabel('Total Seats')
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    plt.show()

#Average- and total seat capacity for sprinters and intercity's
def traintypes_avg_total():
    total_intercity = 0
    for i in intercities['Seats']:
        total_intercity += i
    intercity_avg = (total_intercity/len(intercities['Seats']))

    total_sprinter = 0
    for i in sprinters['Seats']:
        total_sprinter += i
    sprinter_avg = total_sprinter/len(sprinters['Seats'])

    print(f'The total amount of seats per week in intercities is {total_intercity}')
    print(f'The total amount of seats per week in sprinters is {total_sprinter}')
    print(f'The average amount of seats per week in intercities is {intercity_avg}')
    print(f'The average amount of seats per week in sprinters is {sprinter_avg}')

#Graph of the total seats for sprinters and intercity's vs the day of the week
def traintypes_graph():
    total_days_intercities = []
    total_days_sprinters = []
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    data_intercities = [monday_intercity, tuesday_intercity, wednesday_intercity, thursday_intercity, friday_intercity, saturday_intercity, sunday_intercity]
    data_sprinters = [monday_sprinter, tuesday_sprinter, wednesday_sprinter, thursday_sprinter, friday_sprinter, saturday_sprinter, sunday_sprinter]
    for i in data_intercities:
        total_seats = i['Seats'].sum()
        total_days_intercities.append(total_seats)

    for i in data_sprinters:
        total_seats = i['Seats'].sum()
        total_days_sprinters.append(total_seats)
    
    plt.figure(figsize=(10, 6))
    plt.plot(days, total_days_intercities, marker='o', linestyle='-', color='skyblue', label = 'Intercity', linewidth=2, markersize=8)
    plt.plot(days, total_days_sprinters, marker='o', linestyle='-', color='red', label = 'Sprinter', linewidth=2, markersize=8)
    plt.title('Total Seats per Day')
    plt.xlabel('Days of the Week')
    plt.ylabel('Total Seats')
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    plt.legend()
    plt.show()

#The maximum and minimum differences in seat capacity during the week per traject
def difference_total_week():
    week = pd.concat([monday, tuesday, wednesday, thursday, friday, saturday, sunday], axis=0)
    counter = 0
    df = []
    for index, row in week.iterrows():
        print(counter)
        counter += 1
        From = row['From']
        To = row['To']
            
        maxvalue = float('-inf') 
        minvalue = float('inf') 
            
        for x in range(len(week)):
            current_from = week.iloc[x]['From']
            current_to = week.iloc[x]['To']
                
            if From == current_from and To == current_to:
                current_seat_value = week.iloc[x]['Seats']
                    
                if pd.notnull(current_seat_value):
                    if current_seat_value > maxvalue:
                        maxvalue = current_seat_value
                    if current_seat_value < minvalue:
                        minvalue = current_seat_value
            
        if maxvalue != float('-inf') and minvalue != float('inf'):
            difference = maxvalue - minvalue
            df.append({
                'From': From,
                'To': To,
                'Difference': difference,
                'Maximum seats': maxvalue,
                'Minimum seats': minvalue
                })

    df2 = pd.DataFrame(df)
    df_sorted = df2.sort_values(by = 'Difference', ascending = False) #Sort the dataframe from high to low
    df_sorted_clean = df_sorted.drop_duplicates()                     #Remove all the duplicate values
    
    for index1, row1 in stations.iterrows():
        i = row1['code']
        name = row1['name_long'] 

        for index2, row2 in df_sorted_clean.iterrows():
            j = row2['From']
            if i == j:
                df_sorted_clean.at[index2, 'From'] = name        
            
            k = row2['To']
            if i == k:
                df_sorted_clean.at[index2, 'To'] = name
    
    df_sorted_clean.to_csv('Max difference capacity.csv', index = False)

difference_total_week()


#Difference in seat capacity between randstad and non-randstad average
def difference_randstad():
    df1 = pd.read_csv(randstad)
    df2 = pd.read_csv(week_trajectory, index_col =  'Unnamed: 0')
    Randstadvalues = df1['Randstad'].value_counts()[1.0]
    notRandstandvalues = df1['Randstad'].value_counts()[0.0]

    Randstadtotal = 0
    notRandstadtotal = 0

    for i in range(len(df2)):
        From = df2['From'].iloc[i]
        To = df2['To'].iloc[i]
    
        #Deciding if the station are in or outside the randstad
        From_index = df1[df1['Code'] == From].index
        To_index = df1[df1['Code'] == To].index
        if not From_index.empty and not To_index.empty:
            if df1['Randstad'].iloc[From_index[0]] == 1 or df1['Randstad'].iloc[To_index[0]] == 1:
                Randstadtotal += df2['Seats'].iloc[i]
            else:
                notRandstadtotal += df2['Seats'].iloc[i]

    Randstadavg = Randstadtotal / Randstadvalues
    notRandstadavg = notRandstadtotal / notRandstandvalues
    print(Randstadavg)
    print(notRandstadavg)




