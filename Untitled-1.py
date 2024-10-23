monday = pd.read_csv('OutputData/SeatsPerTrajectoryMonday.csv', index_col = 'Unnamed: 0')
tuesday = pd.read_csv('OutputData/SeatsPerTrajectoryTuesday.csv', index_col = 'Unnamed: 0')
wednesday = pd.read_csv('OutputData/SeatsPerTrajectoryWednesday.csv', index_col = 'Unnamed: 0')
thursday = pd.read_csv('OutputData/SeatsPerTrajectoryThursday.csv', index_col = 'Unnamed: 0')
friday = pd.read_csv('OutputData/SeatsPerTrajectoryFriday.csv', index_col = 'Unnamed: 0')
saturday = pd.read_csv('OutputData/SeatsPerTrajectorySaturday.csv', index_col = 'Unnamed: 0')
sunday = pd.read_csv('OutputData/SeatsPerTrajectorySunday.csv', index_col = 'Unnamed: 0')



week = pd.concat([monday, tuesday, wednesday, thursday, friday, saturday, sunday], axis = 1)
#print(week)

df = []
count = 0

for i in week.iloc[:, 14]:
    if count == 1:
        break
    count += 1
    if isinstance(i, float):
        index = (week.index[week.iloc[:, 14] == i])[0]
        maxvalue = float('-inf')
        minvalue = float('inf')
        From = week.iat[index, 13]
        To = week.iat[index, 12]

        seat_columns = [2, 5, 8, 11, 17, 20]
        for j in seat_columns:
            From_col = j-2
            To_col = j-1

            for x in range(len(week)):
                current_from = week.iloc[x, From_col] 
                current_to = week.iloc[x, To_col] 
                if From == current_from and To == current_to:
                    print('Current from is', current_from)
                    current_seat_value = week.iloc[x, j]  
                    print(current_seat_value)
                    print(maxvalue)
                    if current_seat_value > maxvalue:

                        maxvalue = current_seat_value
                    if count == 0:
                        minvalue = current_seat_value
                    elif current_seat_value < minvalue:
                        minvalue = current_seat_value
        
        difference = maxvalue - minvalue

        df.append({
            'From': From,
            'To': To,
            'Difference': difference,
            'Maximum seats': maxvalue,
            'Minimum seats': minvalue
                })
    df2 = pd.DataFrame(df)
    print(df2)