import pandas as pd
from datetime import datetime
from pytz import UTC
import glob
from tqdm import tqdm

def generate_min_dataframes(input_file, timeframe):
    # Read tick data from CSV file
    tick_data = pd.read_csv(input_file)
    # tick_data = tick_data.head(100000)

    # Convert 'Timestamp' column to datetime
    tick_data['Timestamp'] = pd.to_datetime(tick_data['Timestamp'])

    # Set 'Timestamp' as the index
    tick_data.set_index('Timestamp', inplace=True)

    # Group tick data by minute and store in a dictionary
    minute_dataframes = {}
    for name, group in tick_data.groupby(pd.Grouper(freq=timeframe+'T')):
        minute_dataframes[name] = group

    return minute_dataframes

def is_between_time(timestamp_str):
    global start_time, end_time
    # Parse the timestamp string into a datetime object
    timestamp_dt = datetime.fromisoformat(timestamp_str.rstrip("Z"))

    # Extract the hour from the datetime object
    hour = int(timestamp_dt.hour)
    if hour >= start_time and hour <= end_time:
        return True
    return False
    

def create_candle(df):
    price = df['Bid'].values
    openPrice = price[0]
    closePrice = price[-1]
    high = max(price)
    low = min(price)
    last_row = df.iloc[-1]
    return [openPrice, closePrice, high, low,last_row[0]]
    
def checkCandleBody(cad):
    size = abs(cad[0] - cad[1])
    upCandle = 'RED'
    if (cad[0] - cad[1]) < 0: 
        # if True then its a GREEN candle
        upCandle = "GREEN"
        
    return [size,upCandle]

def writeData(data_, cnter):
    global ComboData
    ComboData.append(cnter)
    #-------input('Order Closed!! ')
    # #-------print('here')

def v2Analysis(candles):
    global oldCandlePriceMove
    ##-------print('\n\n')
    ##-------print(candles)
    cadColor = candles[0][1]
    
    bodySize = 0
    for cad in candles:
        if cadColor != cad[1]:
            ##-------print('Color missmatch')
            return False
        bodySize += cad[0]
    
    if oldCandlePriceMove <= bodySize:
        ##-------print('Color matched and Body size matched too, Body Size: ',bodySize)
        return True
    else:
        ##-------print('Color Matched but body size isnot! ')
        return False


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


def combine_csv_files(output_file):
    # Get a list of all CSV files in the input folder
    csv_files = glob.glob( './*.csv')
    print(csv_files)
   
    # Initialize an empty list to hold DataFrames
    dfs = []
    
    # Read each CSV file and append its DataFrame to the list
    for csv_file in csv_files:
        df = pd.read_csv(csv_file)
        dfs.append(df)
    
    # Concatenate all DataFrames into a single DataFrame
    combined_df = pd.concat(dfs, ignore_index=True)
    
    # Write the combined DataFrame to a new CSV file
    # combined_df = sort_dataframe_by_datetime(combined_df, "Timestamp")
    combined_df.to_csv(output_file, index=False)
    print("Combined CSV file saved successfully!")


if __name__ == "__main__":
    timeframe = "15"
    pairName = "XAUUSD"
    
    finalcomboData = []
    
    # [numberOfOldCandleColor, oldCandlePriceMove, FinalCandleSize]
    combinations = [[3,2,4],[2,2,3],[1,2,2],[1,3,2]]
    
    
    # --------------- Dont touch at all!!  ------------------- 
    input_file = "combo.csv"   
    combine_csv_files(input_file)
    minute_dataframes = generate_min_dataframes(input_file,timeframe)
    for combo in tqdm(combinations):
        print(combo)
        # new inputs
        numberOfOldCandleColor = combo[0]
        oldCandlePriceMove = combo[1] # points
        FinalCandleSize =  combo[2] # points
        
        ComboData = []
        # ComboData.append(numberOfOldCandleColor)
        # ComboData.append(oldCandlePriceMove)
        # ComboData.append(FinalCandleSize)
        
        start_time = 0
        end_time = 24
        tpReduce = 0.1
        middleLinePosition = 1
        # dont touch below -----------------
        allOrders = []
        data = []
        ifOrderRunning = False
        orderType = False # true = BUY and False = SELL
        sl = 0
        tp = 0
        sl2 = 0
        tp2 = 0
        cadBodySize = 0
        fileName = "{}_ci_{}m".format(pairName, timeframe  )
            
        
        zeroLine = 0
        middleLine = 0
        orderCounter = 0
        candlesDataHub = []
        
        
        # Example: Accessing dataframes for each minute
        for minute, dataframe in minute_dataframes.items():
            
            # print(f"Minute: {minute}")
            
            if not is_between_time(str(minute)):
                print('skip!! - ',minute)
                # input('here')
                continue  
            
            try:
                candle = create_candle(dataframe)
            except:
                ##-------print("Error creating Candle",minute)
                # ##-------print(dataframe.head())
                # #-------input("XXX")
                continue

            candleInfo = checkCandleBody(candle)
            # candleInfo.append(minute)
            candlesDataHub.append(candleInfo)
            ##-------print(candleInfo)
            
            if not ifOrderRunning:
                # at least some old candle needed
                if len(candlesDataHub) > numberOfOldCandleColor :
                    cads = candlesDataHub[-numberOfOldCandleColor-1:-1]
                    prevCandleFlag = v2Analysis(cads)
                    if prevCandleFlag:
                        candleFlag = cads[0][1]
                        if candleFlag == candlesDataHub[-1][1]: # change here.......... == Same color candle or != differnt color
                            if candlesDataHub[-1][0] > FinalCandleSize :
                                ##-------print(candlesDataHub[-1])
                                # #-------input('xxxx')
                                # print('\n\n\n NEW ORDER !!!!!!! Order! ', minute)
                                # continue
                                zeroLine = candle[1] 
                                ifOrderRunning = True
                                orderType = candlesDataHub[-1][1]
                                orderCounter = 0
                                cadBodySize = candlesDataHub[-1][0]
                                if orderType == 'GREEN': # BUY
                                    sl = candle[1] - (cadBodySize*2)
                                    tp = candle[1] + (cadBodySize* (1-tpReduce))
                                    middleLine = candle[1] - (cadBodySize*middleLinePosition)
                                    #-------print('BUY')
                                    #-------print('Open Price: ', candle[1])
                                    #-------print('middleLine: ', middleLine)
                                    #-------print('SL: ', sl)
                                    #-------print('tp: ', tp)
                                    data = []
                                    data.append(minute)
                                    data.append('BUY')
                                    data.append(candle[1])
                                    data.append(cadBodySize)
                                    data.append(middleLine)
                                    data.append(sl)
                                    data.append(tp)
                                    data.append(0)
                                    data.append(0)
                                    data.append(0)
                                    #-------input('\n\n\n\n\Order Placed next..')
                                    continue
                                else: # SELL
                                    sl = candle[1] + (cadBodySize*2)
                                    tp = candle[1] - (cadBodySize*0.9)
                                    middleLine = candle[1] + (cadBodySize*middleLinePosition)
                                    #-------print('SELL')
                                    #-------print('Open Price: ', candle[1])
                                    #-------print('middle Line: ', middleLine)
                                    #-------print('SL: ', sl)
                                    #-------print('tp: ', tp)
                                    data = []
                                    data.append(minute)
                                    data.append('SELL')
                                    data.append(candle[1])
                                    data.append(cadBodySize)
                                    data.append(middleLine)
                                    data.append(sl)
                                    data.append(tp)
                                    data.append(0)
                                    data.append(0)
                                    data.append(0)
                                    #-------input('\n\n\n\n\Order Placed next..')
                                    continue

            if ifOrderRunning:
                for ind,row in dataframe.iterrows():
                    if orderType == "GREEN": # if its a BUY
                        # check for new order (2,3,4)
                        if row['Bid'] <= middleLine and orderCounter == 0: # order 2 -> SELL
                            #-------print("new SELL Order Price: ", row['Bid'])
                            orderCounter = 1
                            sl2 = tp + (cadBodySize*tpReduce)
                            tp2 = sl + (cadBodySize*tpReduce)
                            data[-3] = sl2
                            data[-2] = tp2
                            data[-1] = orderCounter
                            #-------print('2nd TP: ', tp2)
                            #-------print("2nd SL: ",sl2)
                            #-------input('__2')
                            continue
                        elif  row['Ask'] >= zeroLine and orderCounter == 1:  # order 3 -> BUY
                            #-------print("new Order: ", row['Bid'])
                            orderCounter = 2
                            data[-1] = orderCounter
                            #-------input('__3')
                            continue
                        elif row['Bid'] <= middleLine and orderCounter ==2: # order 4 -> SELL
                            #-------print("new SELL Order Price: ", row['Bid'])
                            orderCounter = 3
                            data[-1] = orderCounter
                            #-------input('__4')
                            continue
                        elif  row['Ask'] >= zeroLine and orderCounter == 3:  # order 5 -> BUY
                            #-------print("new Order: ", row['Bid'])
                            orderCounter = 4
                            data[-1] = orderCounter
                            #-------input('__5')
                            continue
                        elif row['Bid'] <= middleLine and orderCounter ==4: # order 6 -> SELL
                            #-------print("new SELL Order Price: ", row['Bid'])
                            orderCounter = 5
                            data[-1] = orderCounter
                            #-------input('__6')
                            continue
                        elif  row['Ask'] >= zeroLine and orderCounter == 5:  # order 5 -> BUY
                            #-------print("new Order: ", row['Bid'])
                            orderCounter = 6
                            data[-1] = orderCounter
                            #-------input('__7')
                            continue
                        elif row['Bid'] <= middleLine and orderCounter ==6: # order 6 -> SELL
                            #-------print("new SELL Order Price: ", row['Bid'])
                            orderCounter = 7
                            data[-1] = orderCounter
                            #-------input('__8')
                            continue
                        elif  row['Ask'] >= zeroLine and orderCounter == 7:  # order 5 -> BUY
                            #-------print("new Order: ", row['Bid'])
                            orderCounter = 8
                            data[-1] = orderCounter
                            #-------input('__9')
                            continue
                        elif row['Bid'] <= middleLine and orderCounter ==8: # order 6 -> SELL
                            #-------print("new SELL Order Price: ", row['Bid'])
                            orderCounter = 9
                            data[-1] = orderCounter
                            #-------input('__10')
                            continue
                        elif  row['Ask'] >= zeroLine and orderCounter == 9:  # order 5 -> BUY
                            #-------print("new Order: ", row['Bid'])
                            orderCounter = 10
                            data[-1] = orderCounter
                            #-------input('__11')
                            continue
                        elif row['Bid'] <= middleLine and orderCounter ==10: # order 6 -> SELL
                            #-------print("new SELL Order Price: ", row['Bid'])
                            orderCounter = 11
                            data[-1] = orderCounter
                            #-------input('__12')
                            continue
                        
                        if orderCounter == 0 and row['Bid'] >= tp: # for the first order - BUY
                            #-------print('Its a win!! Order 1 ', "Price :", row["Ask"])
                            ifOrderRunning = False
                            data.append('WIN')
                            data.append(row['Bid'])
                            writeData(ComboData, orderCounter)
                            break
                            
                        if orderCounter == 1 and row['Ask'] <= tp2: # for 2nd order - SELL
                            #-------print("its a win!! Order 2", "Price :", row["Ask"])
                            ifOrderRunning = False
                            data.append('WIN')
                            data.append(row['Bid'])
                            writeData(ComboData, orderCounter)
                            break
                            
                        if  orderCounter == 2 and row['Bid'] >= tp: # for 3nd order - BUY
                            #-------print("its a win!! Order 3", "Price :", row["Ask"])
                            ifOrderRunning = False
                            data.append('WIN')
                            data.append(row['Bid'])
                            writeData(ComboData, orderCounter)
                            break
                        
                        if orderCounter == 3 and row['Ask'] <= tp2: # for 4th order
                            #-------print("its a win!! Order 4", "Price :", row["Ask"])
                            ifOrderRunning = False
                            data.append('WIN')
                            data.append(row['Bid'])
                            writeData(ComboData, orderCounter)
                            break
                        
                        if orderCounter == 4 and row['Bid'] >= tp: # for 5th order
                            #-------print("its a win!! Order 5", "Price :", row["Ask"])
                            ifOrderRunning = False
                            data.append('WIN')
                            data.append(row['Bid'])
                            writeData(ComboData, orderCounter)
                            break
                        
                        if orderCounter == 5 and row['Ask'] <= tp2: # for 6th order
                            #-------print("its a win!! Order 6", "Price :", row["Ask"])
                            ifOrderRunning = False
                            data.append('WIN')
                            data.append(row['Bid'])
                            writeData(ComboData, orderCounter)
                            break
                        
                        if orderCounter == 6 and row['Bid'] >= tp: # for 5th order
                            #-------print("its a win!! Order 7", "Price :", row["Ask"])
                            ifOrderRunning = False
                            data.append('WIN')
                            data.append(row['Bid'])
                            writeData(ComboData, orderCounter)
                            break
                        
                        if orderCounter == 7 and row['Ask'] <= tp2: # for 6th order
                            #-------print("its a win!! Order 8", "Price :", row["Ask"])
                            ifOrderRunning = False
                            data.append('WIN')
                            data.append(row['Bid'])
                            writeData(ComboData, orderCounter)
                            break
                        
                        if orderCounter == 8 and row['Bid'] >= tp: # for 5th order
                            #-------print("its a win!! Order 9", "Price :", row["Ask"])
                            ifOrderRunning = False
                            data.append('WIN')
                            data.append(row['Bid'])
                            writeData(ComboData, orderCounter)
                            break
                        
                        if orderCounter == 9 and row['Ask'] <= tp2: # for 6th order
                            #-------print("its a win!! Order 10", "Price :", row["Ask"])
                            ifOrderRunning = False
                            data.append('WIN')
                            data.append(row['Bid'])
                            writeData(ComboData, orderCounter)
                            break
                        
                        if orderCounter == 10 and row['Bid'] >= tp: # for 5th order
                            #-------print("its a win!! Order 11", "Price :", row["Ask"])
                            ifOrderRunning = False
                            data.append('WIN')
                            data.append(row['Bid'])
                            writeData(ComboData, orderCounter)
                            break
                        
                        if orderCounter == 11 and row['Ask'] <= tp2: # for 6th order
                            #-------print("its a win!! Order 12", "Price :", row["Ask"])
                            ifOrderRunning = False
                            data.append('WIN')
                            data.append(row['Bid'])
                            writeData(ComboData, orderCounter)
                            break
                        
                        if orderCounter == 11 and row['Ask'] >= sl2: # for loss order
                            #-------print("its a Loss!! ", "Price :", row["Ask"])
                            ifOrderRunning = False
                            data.append('Loss')
                            data.append(row['Bid'])
                            writeData(ComboData, orderCounter)
                            break
                                
                    
                    if orderType == "RED": # if its a Sell
                            
                        if row['Ask'] >= middleLine and orderCounter == 0: # order 2 - BUY
                            #-------print("new BUY Order Price: ", row['Bid'])
                            orderCounter = 1
                            sl2 = tp + (cadBodySize*tpReduce)
                            tp2 = sl + (cadBodySize*tpReduce)
                            data[-3] = sl2
                            data[-2] = tp2
                            data[-1] = orderCounter
                            #-------print('2nd TP: ', tp2)
                            #-------print("2nd SL: ",sl2) 
                            #-------input('__2') 
                            continue
                        elif  row['Bid'] <= zeroLine and orderCounter == 1:  # order 3 - sell
                            #-------print("new SELL Order Price: ", row['Bid'])
                            orderCounter = 2
                            data[-1] = orderCounter
                            #-------input('__3')
                            continue
                        elif row['Ask'] >= middleLine and orderCounter ==2: # order 4 - buy
                            #-------print("new BUY Order Price: ", row['Bid'])
                            orderCounter = 3
                            data[-1] = orderCounter
                            #-------input('__4')    
                            continue
                        elif  row['Bid'] <= zeroLine and orderCounter == 3:  # order 5 - sell
                            #-------print("new SELL Order Price : ", row['Bid'])
                            orderCounter = 4
                            data[-1] = orderCounter
                            #-------input('__5')
                            continue
                        elif row['Ask'] >= middleLine and orderCounter ==4: # order 6 - buy
                            #-------print("new BUY Order Price: ", row['Bid'])
                            orderCounter = 5
                            data[-1] = orderCounter
                            #-------input('__6')    
                            continue
                        elif  row['Bid'] <= zeroLine and orderCounter == 5:  # order 7 - sell
                            #-------print("new SELL Order Price : ", row['Bid'])
                            orderCounter = 6
                            data[-1] = orderCounter
                            #-------input('__7')
                            continue
                        elif row['Ask'] >= middleLine and orderCounter ==6: # order 6 - buy
                            #-------print("new BUY Order Price: ", row['Bid'])
                            orderCounter = 7
                            data[-1] = orderCounter
                            #-------input('__8')    
                            continue
                        elif  row['Bid'] <= zeroLine and orderCounter == 7:  # order 7 - sell
                            #-------print("new SELL Order Price : ", row['Bid'])
                            orderCounter = 8
                            data[-1] = orderCounter
                            #-------input('__9')
                            continue
                        elif row['Ask'] >= middleLine and orderCounter ==8: # order 6 - buy
                            #-------print("new BUY Order Price: ", row['Bid'])
                            orderCounter = 9
                            data[-1] = orderCounter
                            #-------input('__10')    
                            continue
                        elif  row['Bid'] <= zeroLine and orderCounter == 9:  # order 7 - sell
                            #-------print("new SELL Order Price : ", row['Bid'])
                            orderCounter = 10
                            data[-1] = orderCounter
                            #-------input('__11')
                            continue
                        elif row['Ask'] >= middleLine and orderCounter ==10: # order 6 - buy
                            #-------print("new BUY Order Price: ", row['Bid'])
                            orderCounter = 11
                            data[-1] = orderCounter
                            #-------input('__12')    
                            continue
                        
                        if orderCounter == 0 and row['Ask'] <= tp: # for the first order - SELL
                            #-------print('Its a win!! Order 1', "Price :", row["Ask"])
                            data.append('WIN')
                            data.append(row['Bid'])
                            ifOrderRunning = False
                            writeData(ComboData, orderCounter)
                            break
                            
                        if orderCounter == 1 and row['Bid'] >= tp2: # for 2nd order - BUY
                            #-------print("its a win!! Order 2", "Price :", row["Ask"])
                            data.append('WIN')
                            data.append(row['Bid'])
                            ifOrderRunning = False
                            writeData(ComboData, orderCounter)
                            break
                            
                        if  orderCounter == 2 and row['Ask'] <= tp: # for 3nd order - SELL
                            #-------print("its a win!! Order 3", "Price :", row["Ask"])
                            ifOrderRunning = False
                            data.append('WIN')
                            data.append(row['Bid'])
                            writeData(ComboData, orderCounter)
                            break
                        
                        if orderCounter == 3 and row['Bid'] >= tp2: # for 4th order - BUY
                            #-------print("its a win!! Order 4", "Price :", row["Ask"])
                            ifOrderRunning = False
                            data.append('WIN')
                            data.append(row['Bid'])
                            writeData(ComboData, orderCounter)
                            break
                            
                        if  orderCounter == 4 and row['Ask'] <= tp: # for 5nd order - SELL
                            #-------print("its a win!! Order 5", "Price :", row["Ask"])
                            ifOrderRunning = False
                            data.append('WIN')
                            data.append(row['Bid'])
                            writeData(ComboData, orderCounter)
                            break
                        
                        if orderCounter == 5 and row['Bid'] >= tp2: # for 6th order - BUY
                            #-------print("its a win!! Order 6", "Price :", row["Ask"])
                            ifOrderRunning = False
                            data.append('WIN')
                            data.append(row['Bid'])
                            writeData(ComboData, orderCounter)
                            break
                            
                        if  orderCounter == 6 and row['Ask'] <= tp: # for 5nd order - SELL
                            #-------print("its a win!! Order 7", "Price :", row["Ask"])
                            ifOrderRunning = False
                            data.append('WIN')
                            data.append(row['Bid'])
                            writeData(ComboData, orderCounter)
                            break
                        
                        if orderCounter == 7 and row['Bid'] >= tp2: # for 6th order - BUY
                            #-------print("its a win!! Order 8", "Price :", row["Ask"])
                            ifOrderRunning = False
                            data.append('WIN')
                            data.append(row['Bid'])
                            writeData(ComboData, orderCounter)
                            break
                            
                        if  orderCounter == 8 and row['Ask'] <= tp: # for 5nd order - SELL
                            #-------print("its a win!! Order 9", "Price :", row["Ask"])
                            ifOrderRunning = False
                            data.append('WIN')
                            data.append(row['Bid'])
                            writeData(ComboData, orderCounter)
                            break
                        
                        if orderCounter == 9 and row['Bid'] >= tp2: # for 6th order - BUY
                            #-------print("its a win!! Order 10", "Price :", row["Ask"])
                            ifOrderRunning = False
                            data.append('WIN')
                            data.append(row['Bid'])
                            writeData(ComboData, orderCounter)
                            break
                            
                        if  orderCounter == 10 and row['Ask'] <= tp: # for 5nd order - SELL
                            #-------print("its a win!! Order 11", "Price :", row["Ask"])
                            ifOrderRunning = False
                            data.append('WIN')
                            data.append(row['Bid'])
                            writeData(ComboData, orderCounter)
                            break
                        
                        if orderCounter == 11 and row['Bid'] >= tp2: # for 6th order - BUY
                            #-------print("its a win!! Order 12", "Price :", row["Ask"])
                            ifOrderRunning = False
                            data.append('WIN')
                            data.append(row['Bid'])
                            writeData(ComboData, orderCounter)
                            break
                        
                        if orderCounter == 11 and row['Bid'] <= sl2: # for loss order
                            #-------print("its a Loss!!", "Price :", row["Ask"])
                            ifOrderRunning = False
                            data.append('LOSS')
                            data.append(row['Bid'])
                            writeData(ComboData, orderCounter)
                            break    
                            
                            
            # #-------print('-------------------------------')
        
        
        if len(ComboData) > 0:
            tempData = []
            tempData.append(numberOfOldCandleColor)
            tempData.append(oldCandlePriceMove)
            tempData.append(FinalCandleSize)
            tempData.append(len(ComboData))
            tempData.append(max(ComboData))
            finalcomboData.append(tempData)
            df = pd.DataFrame(finalcomboData, columns=['numberOfOldCandleColor', 'oldCandlePriceMove', 'FinalCandleSize','Orders','Max Cycle'])
            df.to_csv('Final_combo_{}.csv'.format(pairName))
        else:
            tempData = []
            tempData.append(numberOfOldCandleColor)
            tempData.append(oldCandlePriceMove)
            tempData.append(FinalCandleSize)
            tempData.append(0)
            tempData.append(0)
            finalcomboData.append(tempData)
            df = pd.DataFrame(finalcomboData, columns=['numberOfOldCandleColor', 'oldCandlePriceMove', 'FinalCandleSize','Orders','Max Cycle'])
            df.to_csv('Final_combo_{}.csv'.format(pairName))
            
            
            