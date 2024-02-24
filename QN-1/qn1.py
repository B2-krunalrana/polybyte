import requests
import pandas as pd
from datetime import datetime
import pytz
import ta

def get_data(symbol, start_time, end_time, interval, api_key, api_secret):
    url = f"https://api.bybit.com/v2/public/kline/list?symbol={symbol}&interval={interval}&limit=200"
    headers = {
        'Content-Type': 'application/json',
        'api_key': api_key,
        'api_secret': api_secret
    }

    print()
    print()
    print(url)
    print()
    print()
    response = requests.get(url, headers=headers)
    data = response.json()
    df = pd.DataFrame(data['result'])
    df.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'turnover']
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    df['timestamp'] = df['timestamp'].dt.tz_localize('UTC').dt.tz_convert('Asia/Kolkata')
    df.set_index('timestamp', inplace=True)
    start_timestamp = pd.Timestamp(start_time, tz='Asia/Kolkata')
    end_timestamp = pd.Timestamp(end_time, tz='Asia/Kolkata')
    while df.index[-1] < end_timestamp:
        last_timestamp = df.index[-1]
        url = f"https://api.bybit.com/v2/public/kline/list?symbol={symbol}&interval={interval}&limit=200&from={int(last_timestamp.timestamp())+1}"
        response = requests.get(url, headers=headers)
        data = response.json()
        temp_df = pd.DataFrame(data['result'])
        temp_df.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'turnover']
        temp_df['timestamp'] = pd.to_datetime(temp_df['timestamp'], unit='s')
        temp_df['timestamp'] = temp_df['timestamp'].dt.tz_localize('UTC').dt.tz_convert('Asia/Kolkata')
        temp_df.set_index('timestamp', inplace=True)
        df = pd.concat([df, temp_df])
    df = df[(df.index >= start_timestamp) & (df.index <= end_timestamp)]
    df['VWAP'] = ta.volume.VolumeWeightedAveragePrice(high=df['high'], low=df['low'], close=df['close'], volume=df['volume'], window=15)
    df['MACD'] = ta.trend.macd_diff(close=df['close'])
    return df

start_time = '2021-01-01 00:00:00'
end_time = '2022-12-31 23:59:59'
symbol = 'BTCUSD'
interval = '15m'
api_key = 'SzjZaCcu6FDfr1G3QQ'
api_secret = '5D1Wi0A6l4Kkg3t1pIVSNtqXI8llBHDhxqda'

data = get_data(symbol, start_time, end_time, interval, api_key, api_secret)
print(data)


