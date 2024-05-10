import pandas as pd
import glob
from dateutil.parser import parse

def MM(balance,baseRiskRush, additinonalMuliplierRush,firstOrderPF, evenOrderPF,oddOrderPf):
    results = []
    pf = [oddOrderPf,evenOrderPF,  oddOrderPf ,evenOrderPF,  oddOrderPf ,evenOrderPF,  oddOrderPf ,evenOrderPF,  oddOrderPf ,evenOrderPF, oddOrderPf ,evenOrderPF]
    
    # order - 1
    val = (balance * baseRiskRush)/100
    order1 = (val * additinonalMuliplierRush[0]) 
    results.append([order1/2, order1 * firstOrderPF])
    
    # order - 2
    val = (order1 * (1/pf[1]) ) 
    order2 = (val * additinonalMuliplierRush[1])  
    results.append([order2/2, (order2 * pf[1])-order1])
    
    # order - 3
    val = (order2 * (1/pf[2]) ) - (order1 * pf[0]) 
    order3 = (val * additinonalMuliplierRush[2]) 
    results.append([(order3+order1)/2 , ((order3 * pf[2])+(order1*pf[0])) - (order2)])

    # order - 4
    val = ((order3 * (1/pf[3]) ) + (order1 * (1/pf[3]))) - (order2 * pf[1]) 
    order4 = (val * additinonalMuliplierRush[3])  
    results.append([(order4 + order2)/2 , ((order4 * pf[3])+(order2*pf[1]) )- (order1 + order3)])
    
    # order - 5
    val = ((order2 * (1/pf[4]) ) + (order4 * (1/pf[4]) )) - ((order1 * pf[0]) + (order3 * pf[2]) )
    order5 = (val * additinonalMuliplierRush[4]) 
    results.append([ (order5 + order3 + order1)/2 , ((order5 * pf[4])+(order3 * pf[2])+(order1*pf[0])) - (order2+order4)])

    
    # order - 6
    val = ((order1 * (1/pf[5]) ) + (order3 * (1/pf[5]) ) + (order5 * (1/pf[5]) )) - ((order2 * pf[1]) + (order4 * pf[3]) )
    order6 = (val * additinonalMuliplierRush[5]) 
    results.append([ (order6  + order4 + order2)/2 , ((order6 * pf[5])+(order4 * pf[3])+(order2*pf[1])) - (order1+order3+order5)])
    
    # order - 7
    val = ((order2 * (1/pf[6]) ) + (order4 * (1/pf[6]) ) + (order6 * (1/pf[6]) ) ) - ((order1 * pf[0]) + (order3 * pf[2])+ (order5 * pf[4]) )
    order7 = (val * additinonalMuliplierRush[6]) 
    results.append([ (order7 + order5 + order3 + order1)/2 , ((order7 * pf[6])+(order5 * pf[4])+(order3 * pf[2])+(order1*pf[0])) - (order2+order4+order6)])
    
    # order - 8
    val = ((order1 * (1/pf[7]) ) + (order3 * (1/pf[7]) ) + (order5 * (1/pf[7]) ) + (order7 * (1/pf[7]) )) - ((order2 * pf[1]) + (order4 * pf[3]) + (order6 * pf[5]) )
    order8 = (val * additinonalMuliplierRush[7]) 
    results.append([ (order8 + order2 + order4 + order6)/2 , ((order8 * pf[7])+(order6 * pf[5])+(order4 * pf[3])+(order2*pf[1])) - (order1+order3+order5+order7)])
    
    # order - 9
    val = ((order2 * (1/pf[8]) ) + (order4 * (1/pf[8]) ) + (order6 * (1/pf[8]) )  + (order8 * (1/pf[8]) ) ) - ((order1 * pf[0]) + (order3 * pf[2])+ (order5 * pf[4])+ (order7 * pf[6]) )
    order9 = (val * additinonalMuliplierRush[8]) 
    results.append([ (order9 + order7 + order5 + order3 + order1)/2 , ((order9 * pf[8])+(order7 * pf[6])+(order5 * pf[4])+(order3 * pf[2])+(order1*pf[0])) - (order2+order4+order6+order8)])
    
    
    # order - 10
    val = ((order1 * (1/pf[9]) ) + (order3 * (1/pf[9]) ) + (order5 * (1/pf[9]) ) + (order7 * (1/pf[9]) ) + (order9 * (1/pf[9]) ) ) - ((order2 * pf[1]) + (order4 * pf[3]) + (order6 * pf[5])+ (order8 * pf[7]) )
    order10 = (val * additinonalMuliplierRush[9]) 
    results.append([ (order10 + order4 + order2 + order6 + order8)/2 , ((order10 * pf[9])+(order8 * pf[7])+(order6 * pf[5])+(order4 * pf[3])+(order2*pf[1])) - (order1+order3+order5+order7+order9)])
    
    
    # order - 11
    val = ((order2 * (1/pf[10]) ) + (order4 * (1/pf[10]) ) + (order6 * (1/pf[10]) )  + (order8 * (1/pf[10]) ) + (order10 * (1/pf[10]) ) ) - ((order1 * pf[0]) + (order3 * pf[2])+ (order5 * pf[4])+ (order7 * pf[6]) + (order9 * pf[8]) )
    order11 = (val * additinonalMuliplierRush[10]) 
    results.append([ (order11 + order9 + order7 + order5 + order3 + order1)/2 , ((order11 * pf[10])+(order9 * pf[8])+(order7 * pf[6])+(order5 * pf[4])+(order3 * pf[2])+(order1*pf[0])) - (order2+order4+order6+order8+order10)])
    
    # order - 12
    val = ((order1 * (1/pf[11]) ) + (order3 * (1/pf[11]) ) + (order5 * (1/pf[11]) ) + (order7 * (1/pf[11]) ) + (order9 * (1/pf[11]) ) + (order11 * (1/pf[11]) ) ) - ((order2 * pf[1]) + (order4 * pf[3]) + (order6 * pf[5])+ (order8 * pf[7]) + (order10 * pf[9])  )
    order12 = (val * additinonalMuliplierRush[11]) 
    results.append([ (order12 + order10 + order8 + order6 + order4 + order2)/2 , ((order12 * pf[11])+(order10 * pf[9])+(order8 * pf[7])+(order6 * pf[5])+(order4 * pf[3])+(order2*pf[1])) - (order1+order3+order5+order7+order9+order11)])
    
    results.append([0, ((order1 * pf[0])+(order3*pf[2])+(order5*pf[4])+(order7*pf[6])+(order9*pf[8])+(order11*pf[10]) ) - (order2 + order6 +order4 + order8 + order10 + order12)])
    return results
        
def sort_dataframe_by_datetime(df, datetime_column):
    """
    Sorts the DataFrame based on the specified datetime column.
    
    Parameters:
        df (pandas.DataFrame): The input DataFrame.
        datetime_column (str): The name of the datetime column to sort by.
        
    Returns:
        pandas.DataFrame: The sorted DataFrame.
    """
    if datetime_column not in df.columns:
        print(f"Error: '{datetime_column}' column not found in the DataFrame.")
        return None
    
    # Convert the datetime column to datetime type
    df[datetime_column] = pd.to_datetime(df[datetime_column])
    
    # Sort the DataFrame based on the datetime column
    sorted_df = df.sort_values(by=datetime_column)
    
    return sorted_df


def combine_csv_files(input_folder):
    # Get a list of all CSV files in the input folder
    csv_files = glob.glob( './{}/*.csv'.format(input_folder))
   
    # Initialize an empty list to hold DataFrames
    dfs = []
    
    # Read each CSV file and append its DataFrame to the list
    for csv_file in csv_files:
        df = pd.read_csv(csv_file)
        df['Pair'] = csv_file.replace('./{}/'.format(input_folder),'')
        dfs.append(df)
    
    # Concatenate all DataFrames into a single DataFrame
    combined_df = pd.concat(dfs, ignore_index=True)
    
    # Write the combined DataFrame to a new CSV file
    # combined_df = sort_dataframe_by_datetime(combined_df, "Timestamp")
    # combined_df.to_csv('combined_df.csv', index=False)
    # print("You Know, I love you a lot my love!!! <3 ")
    print("Combined CSV file saved successfully!")
    return combined_df


def is_between_dates(start_date_str, end_date_str, check_date_str):
    try:
        start_date = parse(start_date_str)
        end_date = parse(end_date_str)
        check_date = parse(check_date_str)

        if start_date <= check_date <= end_date:
            return True
        else:
            return False
    except ValueError:
        print("Incorrect datetime format provided.")
        return False

if __name__ == '__main__':
    # inputs  =--------------------
    inputs = {
        # firstPF OddPF EvenPF balance BaseRisk multipliers
        "eur232_ci_v2_15m.csv" : [2,0.4,0.35,100,2,[1, 1.5, 1.4, 1.3, 1.2, 1, 1, 1, 1, 0.8, 0.8, 0.8]],
        'eur232_ci_v2_60m.csv' : [2,0.4,0.35,100,2,[1, 1.5, 1.4, 1.3, 1.2, 1, 1, 1, 1, 0.8, 0.8, 0.8]],
        "chf23_ci_v2_60m (2).csv" : [2,0.4,0.35,100,2,[1, 1.5, 1.4, 1.3, 1.2, 1, 1, 1, 1, 0.8, 0.8, 0.8]],
        'gbp23_ci_v2_15m (2).csv' : [2,0.4,0.35,100,2,[1, 1.5, 1.4, 1.3, 1.2, 1, 1, 1, 1, 0.8, 0.8, 0.8]],
    }
    maxPair = 1
        
    # Example usage:
    input_folder = 'dataFiles'  # Path to the folder containing CSV files
    # output_file = 'combined_data.csv'  # Path for the combined CSV file
    df = combine_csv_files(input_folder)
    df = sort_dataframe_by_datetime(df, "Date")
    
    # print(df.head())
    
    pairs = df['Pair'].values
    pairs = list(set(pairs))
    
    finalBal = 0
    old_st = ''
    old_end = ''
    pairCounter = 0
    alL_data = []
    runningPairs = []
    for ind,row in df.iterrows():
        if old_st != '' and is_between_dates(str(old_st),str(old_end), str(row['Date'])) and pairCounter > maxPair:
            print('Skip Trade Time-> ',str(old_st),str(old_end), str(row['Date']) )
            print("This Pair Is running : ", runningPairs)
            print('current Trade : ',row['Pair'])
            print('\n\n')
            continue
        if old_st != '' and is_between_dates(str(old_st),str(old_end), str(row['Date'])):
            # print("here -----> ",str(old_st),str(old_end), str(row['Date']))
            runningPairs.append(row['Pair'])
            pairCounter+=1
        else:
            # print("next trade -----> ",str(old_st),str(old_end), str(row['Date']))
            pairCounter = 0
            runningPairs = []
            
        try:
            peram = inputs[row['Pair']]
        except Exception as e:
            print("My baby, You didnot add the csv file name on the inputs -> This one is missing! Please add this one babu: ", e)
            exit()
        res = MM(peram[3], peram[4],peram[5], peram[0], peram[2], peram[1])
        data = []
        data.append(row['Pair'])
        data.append(row['Date'])
        indx = row['Order Index']
        data.append(indx)
        bal = round((peram[3] * (res[int(indx)][1]/100)),2)
        data.append(bal)
        finalBal +=  bal
        data.append(finalBal)
        alL_data.append(data)
        
        old_st = row['Date']
        old_end = row['Close Time']
    
    
    df = pd.DataFrame(alL_data, columns=["Pair","date", "index",'Amount in this trade',"Overall balance"])
    df.to_csv('Final Data.csv')
    print('Final balance {}'.format(round(finalBal,2)))
        
        
        
        
        
    
    
    