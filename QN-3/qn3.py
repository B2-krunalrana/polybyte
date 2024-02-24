# 3. Same as 1 but get data for 5 symbols at the same time using threading/multiprocessing
# symbols: BTCUSD, ETHUSD, BITUSD, SOLUSD, XRPUSD



import threading
import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_option_chain(symbol):
    url = f"https://www.nseindia.com/option-chain?symbol={symbol}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', {'id': 'octable'})
        
        # Extracting data from the table
        data = []
        for row in table.find_all('tr'):
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])

        # Creating DataFrame
        headers = data[1]
        df = pd.DataFrame(data[2:], columns=headers)
        return df
    else:
        print(f"Failed to fetch data for symbol {symbol}")
        return None

def fetch_option_chains(symbols):
    threads = []
    option_chains = {}
    for symbol in symbols:
        thread = threading.Thread(target=lambda: option_chains.update({symbol: fetch_option_chain(symbol)}))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    return option_chains

if __name__ == "__main__":
    symbols = ["BTCUSD", "ETHUSD", "BITUSD", "SOLUSD", "XRPUSD"]
    option_chains = fetch_option_chains(symbols)
    for symbol, option_chain in option_chains.items():
        if option_chain is not None:
            option_chain.to_excel(f"{symbol}_option_chain.xlsx", index=False)

# if condition ensure that certain code is only executed when the script is run directly, and not when it's imported as a module into another script.
#  so we can easliy used thsi fucntions in other folders 
            