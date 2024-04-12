import pandas as pd
from datetime import datetime
from pytz import UTC

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
    upCandle = False
    if (cad[0] - cad[1]) < 0: 
        # if True then its a GREEN candle
        upCandle = True
    return size,upCandle

def writeData(dt):
    global allOrders,fileName
    allOrders.append(dt)
    col = ["Date",'Order Type', 'Entry Price', 'Cad Size',"middle line", 'SL - 1 ', 'TP - 1', 'SL - 2', 'TP - 2', 'Order Index', 'Outcome', 'Close Price']
    df = pd.DataFrame(allOrders, columns=col)
    df.to_csv('{}.csv'.format(fileName))
    #--input('Order Closed!! ')
    # #--print('here')
    

if __name__ == "__main__":
    input_file = "Exness_XAUUSD_2023.csv"  # Replace with the path to your input CSV file
    timeframe = "5"
    entryCandle_min = 3
    entryCandle_max = 20
    pairName = "XAUUSD"
    start_time = 0
    end_time = 24
    tpReduce = 0.1
    middleLinePosition = 1
    # dont touch below -----------------
    minute_dataframes = generate_min_dataframes(input_file,timeframe)
    allOrders = []
    data = []
    ifOrderRunning = False
    orderType = False # true = BUY and False = SELL
    sl = 0
    tp = 0
    sl2 = 0
    tp2 = 0
    cadBodySize = 0
    fileName = "{}_c3_{}m".format(pairName, timeframe  )
        
    
    zeroLine = 0
    middleLine = 0
    orderCounter = 0
    
    # Example: Accessing dataframes for each minute
    for minute, dataframe in minute_dataframes.items():
        print(f"Minute: {minute}")
        if not is_between_time(str(minute)):
            print('skip!! - ',minute)
            # input('here')
            continue  
        
        # and is_between_time(str(minute))
        if not ifOrderRunning:
            try:
                candle = create_candle(dataframe)
            except:
                continue
            cadSize , direc = checkCandleBody(candle)
            if cadSize >= entryCandle_min and cadSize <= entryCandle_max:
                #--print('\n\n------------------------------')
                #--print('\n\n Entry!', cadSize, direc, candle)
                zeroLine = candle[1] 
                ifOrderRunning = True
                orderType = direc
                orderCounter = 0
                cadBodySize = cadSize
                if direc: # BUY
                    sl = candle[1] - (cadSize*2)
                    tp = candle[1] + (cadSize* (1-tpReduce))
                    middleLine = candle[1] - (cadSize*middleLinePosition)
                    #--print('BUY')
                    #--print('Open Price: ', candle[1])
                    #--print('middleLine: ', middleLine)
                    #--print('SL: ', sl)
                    #--print('tp: ', tp)
                    data = []
                    data.append(minute)
                    data.append('BUY')
                    data.append(candle[1])
                    data.append(cadSize)
                    data.append(middleLine)
                    data.append(sl)
                    data.append(tp)
                    data.append(0)
                    data.append(0)
                    data.append(0)
                    continue
                else: # SELL
                    sl = candle[1] + (cadSize*2)
                    tp = candle[1] - (cadSize*0.9)
                    middleLine = candle[1] + (cadSize*middleLinePosition)
                    #--print('SELL')
                    #--print('Open Price: ', candle[1])
                    #--print('middle Line: ', middleLine)
                    #--print('SL: ', sl)
                    #--print('tp: ', tp)
                    data = []
                    data.append(minute)
                    data.append('SELL')
                    data.append(candle[1])
                    data.append(cadSize)
                    data.append(middleLine)
                    data.append(sl)
                    data.append(tp)
                    data.append(0)
                    data.append(0)
                    data.append(0)
                    continue
                #--input('next..')
        if ifOrderRunning:
            for ind,row in dataframe.iterrows():
                if orderType: # if its a BUY
                    # check for new order (2,3,4)
                    if row['Bid'] <= middleLine and orderCounter == 0: # order 2 -> SELL
                        #--print("new SELL Order Price: ", row['Bid'])
                        orderCounter = 1
                        sl2 = tp + (cadBodySize*tpReduce)
                        tp2 = sl + (cadBodySize*tpReduce)
                        data[-3] = sl2
                        data[-2] = tp2
                        data[-1] = orderCounter
                        #--print('2nd TP: ', tp2)
                        #--print("2nd SL: ",sl2)
                        #--input('__2')
                        continue
                    elif  row['Ask'] >= zeroLine and orderCounter == 1:  # order 3 -> BUY
                        #--print("new Order: ", row['Bid'])
                        orderCounter = 2
                        data[-1] = orderCounter
                        #--input('__3')
                        continue
                    elif row['Bid'] <= middleLine and orderCounter ==2: # order 4 -> SELL
                        #--print("new SELL Order Price: ", row['Bid'])
                        orderCounter = 3
                        data[-1] = orderCounter
                        #--input('__4')
                        continue
                    elif  row['Ask'] >= zeroLine and orderCounter == 3:  # order 5 -> BUY
                        #--print("new Order: ", row['Bid'])
                        orderCounter = 4
                        data[-1] = orderCounter
                        #--input('__5')
                        continue
                    elif row['Bid'] <= middleLine and orderCounter ==4: # order 6 -> SELL
                        #--print("new SELL Order Price: ", row['Bid'])
                        orderCounter = 5
                        data[-1] = orderCounter
                        #--input('__6')
                        continue
                    
                    if orderCounter == 0 and row['Bid'] >= tp: # for the first order - BUY
                        #--print('Its a win!! Order 1 ', "Price :", row["Ask"])
                        data.append('WIN')
                        data.append(row['Bid'])
                        ifOrderRunning = False
                        writeData(data)
                        break
                        
                    if orderCounter == 1 and row['Ask'] <= tp2: # for 2nd order - SELL
                        #--print("its a win!! Order 2", "Price :", row["Ask"])
                        ifOrderRunning = False
                        data.append('WIN')
                        data.append(row['Bid'])
                        writeData(data)
                        break
                        
                    if  orderCounter == 2 and row['Bid'] >= tp: # for 3nd order - BUY
                        #--print("its a win!! Order 3", "Price :", row["Ask"])
                        ifOrderRunning = False
                        data.append('WIN')
                        data.append(row['Bid'])
                        writeData(data)
                        break
                    
                    if orderCounter == 3 and row['Ask'] <= tp2: # for 4th order
                        #--print("its a win!! Order 4", "Price :", row["Ask"])
                        ifOrderRunning = False
                        data.append('WIN')
                        data.append(row['Bid'])
                        writeData(data)
                        break
                    
                    if orderCounter == 4 and row['Bid'] >= tp: # for 5th order
                        #--print("its a win!! Order 5", "Price :", row["Ask"])
                        ifOrderRunning = False
                        data.append('WIN')
                        data.append(row['Bid'])
                        writeData(data)
                        break
                    
                    if orderCounter == 5 and row['Ask'] <= tp2: # for 6th order
                        #--print("its a win!! Order 6", "Price :", row["Ask"])
                        ifOrderRunning = False
                        data.append('WIN')
                        data.append(row['Bid'])
                        writeData(data)
                        break
                    
                    if orderCounter == 5 and row['Ask'] >= sl2: # for loss order
                        #--print("its a Loss!! ", "Price :", row["Ask"])
                        ifOrderRunning = False
                        data.append('Loss')
                        data.append(row['Bid'])
                        writeData(data)
                        break
                            
                
                if not orderType: # if its a Sell
                        
                    if row['Ask'] >= middleLine and orderCounter == 0: # order 2 - BUY
                        #--print("new BUY Order Price: ", row['Bid'])
                        orderCounter = 1
                        sl2 = tp + (cadBodySize*tpReduce)
                        tp2 = sl + (cadBodySize*tpReduce)
                        data[-3] = sl2
                        data[-2] = tp2
                        data[-1] = orderCounter
                        #--print('2nd TP: ', tp2)
                        #--print("2nd SL: ",sl2) 
                        #--input('__2') 
                        continue
                    elif  row['Bid'] <= zeroLine and orderCounter == 1:  # order 3 - sell
                        #--print("new SELL Order Price: ", row['Bid'])
                        orderCounter = 2
                        data[-1] = orderCounter
                        #--input('__3')
                        continue
                    elif row['Ask'] >= middleLine and orderCounter ==2: # order 4 - buy
                        #--print("new BUY Order Price: ", row['Bid'])
                        orderCounter = 3
                        data[-1] = orderCounter
                        #--input('__4')    
                        continue
                    elif  row['Bid'] <= zeroLine and orderCounter == 3:  # order 5 - sell
                        #--print("new SELL Order Price : ", row['Bid'])
                        orderCounter = 4
                        data[-1] = orderCounter
                        #--input('__5')
                        continue
                    elif row['Ask'] >= middleLine and orderCounter ==4: # order 6 - buy
                        #--print("new BUY Order Price: ", row['Bid'])
                        orderCounter = 5
                        data[-1] = orderCounter
                        #--input('__6')    
                        continue
                    
                    if orderCounter == 0 and row['Ask'] <= tp: # for the first order - SELL
                        #--print('Its a win!! Order 1', "Price :", row["Ask"])
                        data.append('WIN')
                        data.append(row['Bid'])
                        ifOrderRunning = False
                        writeData(data)
                        break
                        
                    if orderCounter == 1 and row['Bid'] >= tp2: # for 2nd order - BUY
                        #--print("its a win!! Order 2", "Price :", row["Ask"])
                        data.append('WIN')
                        data.append(row['Bid'])
                        ifOrderRunning = False
                        writeData(data)
                        break
                        
                    if  orderCounter == 2 and row['Ask'] <= tp: # for 3nd order - SELL
                        #--print("its a win!! Order 3", "Price :", row["Ask"])
                        ifOrderRunning = False
                        data.append('WIN')
                        data.append(row['Bid'])
                        writeData(data)
                        break
                    
                    if orderCounter == 3 and row['Bid'] >= tp2: # for 4th order - BUY
                        #--print("its a win!! Order 4", "Price :", row["Ask"])
                        ifOrderRunning = False
                        data.append('WIN')
                        data.append(row['Bid'])
                        writeData(data)
                        break
                        
                    if  orderCounter == 4 and row['Ask'] <= tp: # for 5nd order - SELL
                        #--print("its a win!! Order 5", "Price :", row["Ask"])
                        ifOrderRunning = False
                        data.append('WIN')
                        data.append(row['Bid'])
                        writeData(data)
                        break
                    
                    if orderCounter == 5 and row['Bid'] >= tp2: # for 6th order - BUY
                        #--print("its a win!! Order 6", "Price :", row["Ask"])
                        ifOrderRunning = False
                        data.append('WIN')
                        data.append(row['Bid'])
                        writeData(data)
                        break
                    
                    if orderCounter == 5 and row['Bid'] <= sl2: # for loss order
                        #--print("its a Loss!!", "Price :", row["Ask"])
                        ifOrderRunning = False
                        data.append('LOSS')
                        data.append(row['Bid'])
                        writeData(data)
                        break    
                        
                        
        # #--print('-------------------------------')
