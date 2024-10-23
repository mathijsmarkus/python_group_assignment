import pandas as pd
import matplotlib.pyplot as plt

randstad = "Randstad-0.0.csv"
week_trajectory = 'OutputData/PlotDataWeekall.csv' 
monday = pd.read_csv('OutputData/PlotData2024-10-07all.csv', index_col='Unnamed: 0')
tuesday = pd.read_csv('OutputData/PlotData2024-10-08all.csv', index_col='Unnamed: 0')
wednesday = pd.read_csv('OutputData/PlotData2024-10-09all.csv', index_col='Unnamed: 0')
thursday = pd.read_csv('OutputData/PlotData2024-10-10all.csv', index_col='Unnamed: 0')
friday = pd.read_csv('OutputData/PlotData2024-10-11all.csv', index_col='Unnamed: 0')
saturday = pd.read_csv('OutputData/PlotData2024-10-12all.csv', index_col='Unnamed: 0')
sunday = pd.read_csv('OutputData/PlotData2024-10-13all.csv', index_col='Unnamed: 0')

def min_max_week():
    df = pd.read_csv(week_trajectory, index_col =  'Unnamed: 0')
    sorted_df= df.sort_values(by = 'Seats', ascending=False)
    print(sorted_df.head(10))
    print(sorted_df.tail(10)) 


def graph_differences():
    total_days = []
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    data = [monday, tuesday, wednesday, thursday, friday, saturday, sunday]
    for i in data:
        total_seats = i['Seats'].sum()
        total_days.append(total_seats)
    
    plt.figure(figsize=(10, 6))
    plt.line(days, total_days, color='skyblue')
    plt.title('Total Seats per Day')
    plt.xlabel('Days of the Week')
    plt.ylabel('Total Seats')
    plt.xticks(rotation=45)
    plt.grid(axis='y')



def difference_week_top10():
    week = pd.concat([monday, tuesday, wednesday, thursday, friday, saturday, sunday], axis=0)

    df = []
    for index, row in week.iterrows():
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
    df2.to_excel('Results', sheet_name = 'Difference', index=False)

difference_week_top10()

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




