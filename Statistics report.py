import pandas as pd

randstad = "Randstad-0.0.csv"
week_trajectory = 'OutputData/SeatsPerTrajectoryWeek.csv' 


def min_max_week():
    df = pd.read_csv(week_trajectory, index_col =  'Unnamed: 0')
    sorted_df= df.sort_values(by = 'Seats', ascending=False)
    print(sorted_df.head(10))
    print(sorted_df.tail(10)) 

#Difference during the week
import pandas as pd

# Load the CSV files for each day of the week
monday = pd.read_csv('OutputData/SeatsPerTrajectoryMonday.csv', index_col='Unnamed: 0')
tuesday = pd.read_csv('OutputData/SeatsPerTrajectoryTuesday.csv', index_col='Unnamed: 0')
wednesday = pd.read_csv('OutputData/SeatsPerTrajectoryWednesday.csv', index_col='Unnamed: 0')
thursday = pd.read_csv('OutputData/SeatsPerTrajectoryThursday.csv', index_col='Unnamed: 0')
friday = pd.read_csv('OutputData/SeatsPerTrajectoryFriday.csv', index_col='Unnamed: 0')
saturday = pd.read_csv('OutputData/SeatsPerTrajectorySaturday.csv', index_col='Unnamed: 0')
sunday = pd.read_csv('OutputData/SeatsPerTrajectorySunday.csv', index_col='Unnamed: 0')

# Concatenate data for the whole week
week = pd.concat([monday, tuesday, wednesday, thursday, friday, saturday, sunday], axis=0)

# Initialize a list to store results
df = []
# Iterate over each row in the week dataframe
for index, row in week.iterrows():
    From = row['From']
    To = row['To']
        
        # Initialize max and min seat values
    maxvalue = float('-inf')  # Start with negative infinity
    minvalue = float('inf')   # Start with positive infinity
        
        # Go over all rows again to find matching From/To pairs and compare seat values
    for x in range(len(week)):
        current_from = week.iloc[x]['From']
        current_to = week.iloc[x]['To']
            
            # If the current From/To pair matches the original
        if From == current_from and To == current_to:
            current_seat_value = week.iloc[x]['Seats']
                
                # Ensure the seat value is valid and compare it to max/min values
            if pd.notnull(current_seat_value):
                if current_seat_value > maxvalue:
                    maxvalue = current_seat_value
                if current_seat_value < minvalue:
                    minvalue = current_seat_value
        
        # If valid max and min values were found, calculate the difference
    if maxvalue != float('-inf') and minvalue != float('inf'):
        difference = maxvalue - minvalue
        df.append({
            'From': From,
            'To': To,
            'Difference': difference,
            'Maximum seats': maxvalue,
            'Minimum seats': minvalue
            })

# Convert the list of results into a DataFrame
df2 = pd.DataFrame(df)

# Display the resulting DataFrame
print(df2)

df2.sort()

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




