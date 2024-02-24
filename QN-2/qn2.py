# 2. Write code to scrape option chain for given symbol and expiry date from NSE new website and export it to excel
# url: https://www.nseindia.com/option-chain

import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_option_chain(symbol, expiry_date):
    url = "https://www.nseindia.com/option-chain?symbol={}&expiry={}".format(symbol, expiry_date)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    print(response)
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
        print("Failed to fetch data")

def export_to_excel(df, filename):
    df.to_excel(filename, index=False)
    print(f"Data exported to {filename}")

# usage:
symbol = "SBIN"
expiry_date = "24-Feb-2024"
option_chain_data = scrape_option_chain(symbol, expiry_date)
if option_chain_data is not None:
    export_to_excel(option_chain_data, "{}_option_chain_{}.xlsx".format(symbol, expiry_date))
