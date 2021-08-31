
api_key = '612e5f66a5b1200007c6a166'
api_secret = 'b56ac500-e935-4545-8184-5bcddb8980f2'

import pandas as pd
import time
from kucoin.client import Client

client = Client(api_key, api_secret,api_secret)

ticker = client.get_ticker()
df = pd.DataFrame(ticker['ticker'])


usdtTable = df.loc[df['symbol'].str.contains("-USDT")]
newUsdtTable0 = usdtTable[['symbol','buy']]


for k in range(20):
    time.sleep(10)
    
    ticker = client.get_ticker()
    df = pd.DataFrame(ticker['ticker'])
    
    
    usdtTable = df.loc[df['symbol'].str.contains("-USDT")]
    newUsdtTable1 = usdtTable[['symbol','buy']]
    print(newUsdtTable1)
    
    for index, row in newUsdtTable1.iterrows():
        row["buy"] = round((100*(float(row["buy"]) - float(newUsdtTable0.loc[index,'buy']))/ float(newUsdtTable0.loc[index,'buy'])),2)
       
    
    sorted_df = newUsdtTable1.sort_values(by=['buy'], ascending=False)
    print("-----------------------------------")
    print(sorted_df.head(20))



