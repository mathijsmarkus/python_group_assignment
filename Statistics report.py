import pandas as pd

randstad = "Randstad-0.0.csv"
week_trajectory = 'OutputData/SeatsPerTrajectoryWeek.csv' 


def min_max_week():
    df = pd.read_csv(week_trajectory, index_col =  'Unnamed: 0')
    sorted_df= df.sort_values(by = 'Seats', ascending=False)
    print(sorted_df.head(10))
    print(sorted_df.tail(10)) 

#Difference during the week
monday = pd.read_csv('OutputData/SeatsPerTrajectoryMonday.csv', index_col = 'Unnamed: 0')
tuesday = pd.read_csv('OutputData/SeatsPerTrajectoryTuesday.csv', index_col = 'Unnamed: 0')
wednesday = pd.read_csv('OutputData/SeatsPerTrajectoryWednesday.csv', index_col = 'Unnamed: 0')
thursday = pd.read_csv('OutputData/SeatsPerTrajectoryThursday.csv', index_col = 'Unnamed: 0')
friday = pd.read_csv('OutputData/SeatsPerTrajectoryFriday.csv', index_col = 'Unnamed: 0')
saturday = pd.read_csv('OutputData/SeatsPerTrajectorySaturday.csv', index_col = 'Unnamed: 0')
sunday = pd.read_csv('OutputData/SeatsPerTrajectorySunday.csv', index_col = 'Unnamed: 0')



week = pd.concat([monday, tuesday, wednesday, thursday, friday, saturday, sunday], axis = 1)
print(week)

df = pd.DataFrame(columns=['From', 'To', 'Difference', 'Maximum seats', 'Minimum seats'])
for i in week.iloc[:, 14]:
    if isinstance(i, float):
        index = df.index[df[14] == i]
        maxvalue = week.iloc[index, 2]
        minvalue = week.iloc[index, 2]

        seat_columns = [2, 5, 8, 11, 17, 20]
        for j in seat_columns:
            if week.iloc[value, j] > maxvalue:
                maxvalue = week.iloc[value, j]
            if week.iloc[value,j] < minvalue:
                minvalue = week.iloc[value,j]
    
        From = week.iloc[value, 0]
        To = week.iloc[value, 1]
        difference = maxvalue - minvalue

        df = df.append({
            'From': From,
            'To': To,
            'Difference': difference,
            'Maximum seats': maxvalue,
            'Minimum seats': minvalue
        }, ignore_index=True)

print(df)






#df1 = []
#for i in list1:
    #for j in i:
        #df1['Unnamed: 0'] = 
        #maxvalue = 0
        #minvalue = None
        #if j > maxvalue:
            #maxvalue = j
        #if minvalue == None:
            #minvalue = j
        #elif j < minvalue:
            #minvalue = j

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




