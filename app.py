import pandas as pd


if __name__ == '__main__':
    
    fileName = 'nzdcad_60m.csv'
    df = pd.read_csv(fileName)
    
    outcome = list(df['Outcome'].values)
    
    win = outcome.count('WIN')
    print('\n___________\n')
    print('Win Rate Analysis')
    print('\n___________\n')
    print('Total Trade: ', len(outcome))
    print('Total win: ', win)
    print('Total Loss: ', len(outcome)-win)
    print("win rate %: ",round( (win /len(outcome))*100,2) )
    print('\n___________\n')
    
    print('Number Of Cycles ')
    print('\n___________\n')
    orders = list(df['Order Index'].values)
    for id in range(0,4):
        temp = orders.count(id)
        print("Cycle {} : {} Times ({}%)".format(id, temp, round((temp/len(orders))*100,2)))
        