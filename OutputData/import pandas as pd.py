import pandas as pd
import matplotlib.pyplot as plt

randstad = "Randstad-0.0.csv"
week_trajectory = 'PlotDataWeekall.csv' 
monday = pd.read_csv('PlotData2024-10-07all.csv', index_col='Unnamed: 0')
tuesday = pd.read_csv('PlotData2024-10-08all.csv', index_col='Unnamed: 0')
wednesday = pd.read_csv('PlotData2024-10-09all.csv', index_col='Unnamed: 0')
thursday = pd.read_csv('PlotData2024-10-10all.csv', index_col='Unnamed: 0')
friday = pd.read_csv('PlotData2024-10-11all.csv', index_col='Unnamed: 0')
saturday = pd.read_csv('PlotData2024-10-12all.csv', index_col='Unnamed: 0')
sunday = pd.read_csv('PlotData2024-10-13all.csv', index_col='Unnamed: 0')

monday_sprinter = pd.read_csv('PlotData2024-10-07sprinters.csv', index_col='Unnamed: 0')
tuesday_sprinter = pd.read_csv('PlotData2024-10-08sprinters.csv', index_col='Unnamed: 0')
wednesday_sprinter = pd.read_csv('PlotData2024-10-09sprinters.csv', index_col='Unnamed: 0')
thursday_sprinter = pd.read_csv('PlotData2024-10-10sprinters.csv', index_col='Unnamed: 0')
friday_sprinter = pd.read_csv('PlotData2024-10-11sprinters.csv', index_col='Unnamed: 0')
saturday_sprinter = pd.read_csv('PlotData2024-10-12sprinters.csv', index_col='Unnamed: 0')
sunday_sprinter = pd.read_csv('PlotData2024-10-13sprinters.csv', index_col='Unnamed: 0')

monday_intercity = pd.read_csv('PlotData2024-10-07intercities.csv', index_col='Unnamed: 0')
tuesday_intercity = pd.read_csv('PlotData2024-10-08intercities.csv', index_col='Unnamed: 0')
wednesday_intercity = pd.read_csv('PlotData2024-10-09intercities.csv', index_col='Unnamed: 0')
thursday_intercity = pd.read_csv('PlotData2024-10-10intercities.csv', index_col='Unnamed: 0')
friday_intercity = pd.read_csv('PlotData2024-10-11intercities.csv', index_col='Unnamed: 0')
saturday_intercity = pd.read_csv('PlotData2024-10-12intercities.csv', index_col='Unnamed: 0')
sunday_intercity = pd.read_csv('PlotData2024-10-13intercities.csv', index_col='Unnamed: 0')

intercities = pd.read_csv('PlotDataWeekintercities.csv', index_col='Unnamed: 0')
sprinters = pd.read_csv('PlotDataWeeksprinters.csv', index_col='Unnamed: 0')

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


def difference_traintypes():
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

def graph_differences():
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

graph_differences()