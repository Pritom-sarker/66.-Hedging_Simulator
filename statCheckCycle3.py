import pandas as pd
import pandas as pd


def count_losses_per_period(csv_file):
    # Read CSV file
    df = pd.read_csv(csv_file)

    # Convert 'Date' column to datetime
    df['Date'] = pd.to_datetime(df['Date'])

    # Extract week number from the date
    df['Week'] = df['Date'].dt.strftime('%Y-%U')

    # Extract month and year from the date
    df['Month'] = df['Date'].dt.strftime('%Y-%m')

    # Count the number of 'LOSS' per week
    losses_per_week = df.groupby(['Week', 'Outcome']).size().unstack(fill_value=0).loc[:, 'LOSS']

    # Count the number of 'LOSS' per month
    losses_per_month = df.groupby(['Month', 'Outcome']).size().unstack(fill_value=0).loc[:, 'LOSS']

    # Count the number of weeks with losses
    weeks_with_loss = (losses_per_week > 0).sum()

    # Count the number of weeks without losses
    weeks_without_loss = (losses_per_week == 0).sum()

    return losses_per_week, losses_per_month, weeks_with_loss, weeks_without_loss


def max_back_to_back_occurrence(lst):
    if len(lst) < 2:
        return 0

    max_consecutive_count = 0
    consecutive_count = 1

    for i in range(1, len(lst)):
        if lst[i] == "LOSS" and lst[i] == lst[i - 1]:
            consecutive_count += 1
        else:
            max_consecutive_count = max(max_consecutive_count, consecutive_count)
            consecutive_count = 1

    max_consecutive_count = max(max_consecutive_count, consecutive_count)

    return max_consecutive_count


def count_rows_at_hour(csv_file, hour):
    # Read the CSV file
    df = csv_file

    # Parse the 'Date' column as datetime
    df['Date'] = pd.to_datetime(df['Date'])

    # Extract the hour from the datetime and count rows at the specified hour
    rows_at_hour = df[df['Date'].dt.hour == hour]

    return len(rows_at_hour)

def MM(dropdown):
    
    results = []
    
    # order - 1
    val = (balance * baseRisk)/100
    order1 = (val * additinonalMuliplier[0]) # + (dropdown/pf[0])
    results.append([order1, order1 * pf[0]])
    
    # order - 2
    val = (order1 * (1/pf[1]) ) 
    order2 = (val * additinonalMuliplier[1])  
    results.append([order2, (order2 * pf[1])-order1])
    
    # order - 3
    val = (order2 * (1/pf[2]) ) - (order1 * pf[0]) 
    order3 = (val * additinonalMuliplier[2]) 
    results.append([order3 , ((order3 * pf[2])+(order1*pf[0])) - (order2)])

    # order - 4
    val = ((order3 * (1/pf[3]) ) + (order1 * (1/pf[3]))) - (order2 * pf[1]) 
    order4 = (val * additinonalMuliplier[3])  
    results.append([order4 , ((order4 * pf[3])+(order2*pf[1]) )- (order1 + order3)])
    
    # order - 5
    val = ((order2 * (1/pf[4]) ) + (order4 * (1/pf[4]) )) - ((order1 * pf[0]) + (order3 * pf[2]) )
    order5 = (val * additinonalMuliplier[4]) 
    results.append([order5 , ((order5 * pf[4])+(order3 * pf[2])+(order1*pf[0])) - (order2+order4)])

    
    # order - 6
    val = ((order1 * (1/pf[5]) ) + (order3 * (1/pf[5]) ) + (order5 * (1/pf[5]) )) - ((order2 * pf[1]) + (order4 * pf[3]) )
    order6 = (val * additinonalMuliplier[5]) 
    results.append([order6 , ((order6 * pf[5])+(order4 * pf[3])+(order2*pf[1])) - (order1+order3+order5)])
    
    
    results.append([0, ((order1 * pf[0])+(order3*pf[2])+(order5*pf[4]) ) - (order2 + order6 +order4)])
    return results

def analyze_weekly_performance(csv_file):
    # Read CSV file
    df = csv_file

    # Convert 'Date' column to datetime
    df['Date'] = pd.to_datetime(df['Date'])

    # Extract week number from the date
    df['Week'] = df['Date'].dt.strftime('%Y-%U')

    # Group by week and calculate aggregate metrics
    weekly_metrics = df.groupby('Week').agg({
        'Balance': ['mean', 'max', 'min'],
        'Dropdown': 'max'
    })

    # Find the week with maximum gain
    max_gain_week = weekly_metrics.loc[weekly_metrics[('Balance', 'max')].idxmax()]

    # Find the week with minimum gain
    min_gain_week = weekly_metrics.loc[weekly_metrics[('Balance', 'min')].idxmin()]

    return weekly_metrics, max_gain_week, min_gain_week


if __name__ == '__main__':
    
    fileName = 'XAUUSD_c3_5m.csv'
    baseRisk = 3
    pf = [0.45,0.45, 0.45 ,0.45, 0.45 ,0.45]
    additinonalMuliplier = [1,1.5 ,1.2,1.1,1,1]
    fee = 2
    globalBalance = 10000
    highOrder = 100 # if u put 2, mean 2X of the balance , put 100 if u dont wanna use it
    # dont touch below --------------- 
    balance = 100
    df = pd.read_csv(fileName)
    
    # Convert 'Date' column to datetime
    df['Date'] = pd.to_datetime(df['Date'])

    # Sort DataFrame by date
    df.sort_values(by='Date', inplace=True)

    print(df.head())
    outcome = list(df['Outcome'].values)
    
    win = outcome.count('WIN')
    print('\n___________\n')
    print('Win Rate Analysis')
    print('\n___________\n')
    
    print('Total Trade: ', len(outcome))
    print('Total win: ', win)
    print('Total Loss: ', len(outcome)-win)
    print("Back to Back Loss: ", max_back_to_back_occurrence(outcome))
    print("win rate %: ",round( (win /len(outcome))*100,2) )
    
    
    print('\n___________\n')
    print('Number Of Cycles ')
    print('\n___________\n')
    orders = list(df['Order Index'].values)
    for id in range(0,6):
        temp = orders.count(id)
        print("Cycle {} : {} Times ({}%)".format(id+1, temp, round((temp/len(orders))*100,2)))
        
    print('\n___________\n')
    print('Hour calculation')
    print('\n___________\n')
    
    for ix in range(0,25):
        hour_8_count = count_rows_at_hour(df, ix)
        print('UTC {} : {} Times'.format(ix,hour_8_count ))
        
    print('\n___________\n')
    print('MM calculation')
    print('\n___________\n')
    # mm cal
    newBal = balance
    maxBal = balance
    all_data = []
    dropdowns = []
    dropDownCounter = 0
    lastDrowdown = 0
    eachStepDropdown = 0
    for ind, row in df.iterrows():
        data = []
        out = row['Outcome']
        indx = row['Order Index']
        
        # reset dropdown
        if maxBal == newBal:
            dropDownCounter = 0
            lastDrowdown = 0
            
        # when we have dropdown for the first time
        if dropDownCounter == 0 and abs(maxBal - newBal) > 1:
            dropDownCounter+=1 
            lastDrowdown =  abs(maxBal - newBal)
            eachStepDropdown = lastDrowdown/fee
            # print('0',eachStepDropdown)
        
        # if we have loss then it will re calculate again 
        if dropDownCounter > 0 and lastDrowdown <  abs(maxBal - newBal):
            dropDownCounter=1 
            lastDrowdown =  abs(maxBal - newBal)
            eachStepDropdown = lastDrowdown/fee
            # print('1',eachStepDropdown)
            
        if  dropDownCounter != 0: #dropDownCounter < fee+1 and
            dropDownCounter+=1 
            drp = eachStepDropdown
            # print('Here!!')
        else: 
            drp = 0
            
        results = MM(drp)
        temp = abs(maxBal - newBal)
        dropdowns.append(temp)
        data.append(row['Order Index'])
        if out == 'WIN':
            data.append('WIN')
            try:
                temp1 = round(results[int(indx)][0],2)
            except:
                continue
            if temp1 > highOrder * balance:
                print('High Order Value!! ')
                exit()
            newBal +=  (balance * (results[int(indx)][1]/100))
            data.append(round(results[int(indx)][1],2))
        else:
            data.append('LOSS')
            temp1 = round(results[-1][0],2)
            if temp1 > highOrder* balance:
                print('High Order Value!! ')
                exit()
            newBal += (balance * (results[-1][1]/100))
            data.append(round(results[-1][1],2))
        if (newBal + globalBalance) < 0:
            print(' Margin call! Fuck!!! ')
            break
        if maxBal < newBal:
            maxBal = newBal
        
        data.append(round(newBal,2))
        data.append(temp)
        data.append(temp1)
        data.append(drp)
        all_data.append(data)
    
    col = ['Cycle','Outcome']
    col.append('Gain')
    col.append('Balance')
    col.append('Dropdown')
    col.append('Order Size')
    col.append('additional amount!')
    df1 = pd.DataFrame(all_data, columns= col)
    df1.to_csv('final_{}'.format(fileName))
    print('FInal balance (%): ', newBal)
    print('Max Dropdown: ', round(max(dropdowns),2))
    print('\n___________\n')
    print('Loss stats')
    print('\n___________\n')
    exit()
    
    
    losses_per_week, losses_per_month, weeks_with_loss, weeks_without_loss = count_losses_per_period(fileName)
    print("Number of 'LOSS' per week:")
    print(losses_per_week)
    print("\nNumber of 'LOSS' per month:")
    print(losses_per_month)
    print("\nWeeks with loss:", weeks_with_loss)
    print("Weeks without loss:", weeks_without_loss)
    
    
    print('\n___________\n')
    print('overall weeekly stats')
    print('\n___________\n')
  
    weekly_metrics, max_gain_week, min_gain_week = analyze_weekly_performance(df1)

    print("Weekly Metrics:")
    print(weekly_metrics)
    
    
 