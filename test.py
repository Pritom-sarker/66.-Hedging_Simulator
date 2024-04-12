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
    input("Trade Closed!!")
    

if __name__ == "__main__":
    input_file = "Exness_XAUUSD_2024_04.csv"  # Replace with the path to your input CSV file
    timeframe = "15"
    entryCandle_min = 3
    entryCandle_max = 9
    pairName = "XAUUSD"
    start_time = 0
    end_time = 24
    tpReduce = 0.1
    middleLineInput = 1
    
    # dont touch below -----------------
    minute_dataframes = generate_min_dataframes(input_file,timeframe)
    print(minute_dataframes)