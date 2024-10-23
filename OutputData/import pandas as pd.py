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

graph_differences()