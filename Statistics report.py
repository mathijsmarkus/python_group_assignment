import pandas as pd



#Minimum and Maximum seat capacity per week
file_path = 'OutputData/SeatsPerTrajectoryWeek.csv'
df = pd.read_csv(file_path, index_col =  'Unnamed: 0')
sorted_df= df.sort_values(by = 'Seats', ascending=False)
#print(sorted_df.head(10))
#print(sorted_df.tail(10)) 

#Difference during the week
monday = pd.read_csv('OutputData/SeatsPerTrajectoryMonday.csv', index_col = 'Unnamed: 0')
tuesday = pd.read_csv('OutputData/SeatsPerTrajectoryTuesday.csv', index_col = 'Unnamed: 0')
wednesday = pd.read_csv('OutputData/SeatsPerTrajectoryWednesday.csv', index_col = 'Unnamed: 0')
thursday = pd.read_csv('OutputData/SeatsPerTrajectoryThursday.csv', index_col = 'Unnamed: 0')
friday = pd.read_csv('OutputData/SeatsPerTrajectoryFriday.csv', index_col = 'Unnamed: 0')
saturday = pd.read_csv('OutputData/SeatsPerTrajectorySaturday.csv', index_col = 'Unnamed: 0')
sunday = pd.read_csv('OutputData/SeatsPerTrajectorySunday.csv', index_col = 'Unnamed: 0')

list1 = [monday, tuesday, wednesday, thursday, friday, saturday, sunday]

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

#Difference Randstand and not-Randstad
file = pd.read_csv("Randstad-0.0.csv")
Randstadvalues = file['Randstad'].value_counts()[1.0]
notRandstandvalues = file['Randstad'].value_counts()[0.0]

Randstadtotal = 0
notRandstandtotal = 0

for i in range(len(df)):
    From = df['From'].iloc[i]
    To = df['To'].iloc[i]
    
    #Deciding if the station are in or outside the randstad
    From_index = file[file['Code'] == From].index
    To_index = file[file['Code'] == To].index
    if file['Randstad'].iloc[From_index] == 1.0:
        if file['Randstad'].iloc[To_index] == 1.0:


