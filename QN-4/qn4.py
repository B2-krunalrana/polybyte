import requests
import pandas as pd

def search_symbol_id(query):
    url = "https://www.investing.com/search/service/search"
    params = {
        "search_text": query,
        "term": query,
        "country_id": "0"
    }
    response = requests.get(url, params=params)
    print("Response status code:", response.status_code)
    print("Response content:", response.text)
    if response.status_code == 200:
        data = response.json()
        if data and "quotes" in data:
            for quote in data["quotes"]:
                if quote["type"] == "Index" and quote["pair_type"] == "indices":
                    return quote["pair_id"]
    return None


def fetch_historical_candle_data(symbol, timeframe, start_date, end_date):
    url = "https://www.investing.com/instruments/HistoricalDataAjax"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    params = {
        "interval_sec": timeframe,
        "sort_col": "date",
        "sort_ord": "DESC",
        "action": "historical_data",
        "curr_id": symbol,
        "st_date": start_date,
        "end_date": end_date
    }

    response = requests.post(url, headers=headers, data=params)
    if response.status_code == 200:
        data = response.json()["quotes"]
        df = pd.DataFrame(data, columns=["Date", "Open", "High", "Low", "Close", "Volume"])
        return df
    else:
        print(f"Failed to fetch data for symbol {symbol}")
        return None

if __name__ == "__main__":
    query = "NASDAQ Composite"
    symbol_id = search_symbol_id(query)
    if symbol_id:
        print("Symbol ID:", symbol_id)

        timeframe = "86400"  # Candle timeframe (86400 seconds = 1 day)
        start_date = "01/01/2022"  
        end_date = "02/23/2024"    

        candle_data = fetch_historical_candle_data(symbol_id, timeframe, start_date, end_date)
        if candle_data is not None:
            print(candle_data)
            # Optionally, save data to a CSV file
            candle_data.to_csv("nasdaq_candle_data.csv", index=False)
    else:
        print("Failed to find symbol ID for query:", query)
