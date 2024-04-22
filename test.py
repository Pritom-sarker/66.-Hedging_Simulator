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
    upCandle = 'RED'
    if (cad[0] - cad[1]) < 0: 
        # if True then its a GREEN candle
        upCandle = "GREEN"
        
    return [size,upCandle]

def writeData(dt, dte):
    global allOrders,fileName
    dt.append(dte)
    allOrders.append(dt)
    col = ["Date",'Order Type', 'Entry Price', 'Cad Size',"middle line", 'SL - 1 ', 'TP - 1', 'SL - 2', 'TP - 2', 'Order Index', 'Outcome', 'Close Price',"Close Time"]
    df = pd.DataFrame(allOrders, columns=col)
    df.to_csv('{}.csv'.format(fileName))
    #--input('Order Closed!! ')
    # #--print('here')

def v2Analysis(candles):
    global oldCandlePriceMove
    print('\n\n')
    print(candles)
    cadColor = candles[0][1]
    
    bodySize = 0
    for cad in candles:
        if cadColor != cad[1]:
            print('Color missmatch')
            return False
        bodySize += cad[0]
    
    if oldCandlePriceMove <= bodySize:
        print('Color matched and Body size matched too, Body Size: ',bodySize)
        return True
    else:
        print('Color Matched but body size isnot! ')
        return False

if __name__ == "__main__":
    input_file = "Exness_XAUUSDm_2024.csv"   # Replace with the path to your input CSV file
    timeframe = "15"
    pairName = "XAUUSD"
    
    # new inputs
    numberOfOldCandleColor = 3
    oldCandlePriceMove = 5 # points
    FinalCandleSize =  3 # points
    
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
    fileName = "{}_ci_{}m".format(pairName, timeframe  )
        
    
    zeroLine = 0
    middleLine = 0
    orderCounter = 0
    candlesDataHub = []
    
    
    # Example: Accessing dataframes for each minute
    for minute, dataframe in minute_dataframes.items():
        try:
            candleData = create_candle(dataframe)
        except:
            print("Error creating Candle",minute)
            # print(dataframe.head())
            # input("XXX")
            continue

        candleInfo = checkCandleBody(candleData)
        # candleInfo.append(minute)
        candlesDataHub.append(candleInfo)
        print(candleInfo)
        
        if not ifOrderRunning:
            # at least some old candle needed
            if len(candlesDataHub) > numberOfOldCandleColor :
                cads = candlesDataHub[-numberOfOldCandleColor-1:-1]
                prevCandleFlag = v2Analysis(cads)
                if prevCandleFlag:
                    candleFlag = cads[0][1]
                    if candleFlag != candlesDataHub[-1][1]:
                        if candlesDataHub[-1][0] > FinalCandleSize :
                            print(candlesDataHub[-1])
                            input('xxxx')