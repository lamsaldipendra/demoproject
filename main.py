import os
import csv
from pycoingecko import CoinGeckoAPI

# Initialize CoinGecko API
cg = CoinGeckoAPI()

# Define the path to the CSV file
csv_file_path = "/Users/dipendralamsal/Documents/myproject/prices.csv"

# Function to fetch top crypto data
def fetch_top_crypto_data(top_n=250):
    # Fetch a list of the top N available coins by market cap from CoinGecko
    coins_list = cg.get_coins_markets(vs_currency='usd', per_page=top_n, page=1)
    return coins_list

# Function to save crypto data to a CSV file
def save_data_to_csv(coins_data):
    with open(csv_file_path, mode='a', newline='') as csv_file:
        fieldnames = ['Coin', 'Symbol', 'Price', '1h', '24h', '7d', '24h Volume', 'Mkt Cap', 'FDV', 'Mkt Cap/FDV']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        
        # Write the header if the file is empty
        if os.stat(csv_file_path).st_size == 0:
            writer.writeheader()
        
        # Write the crypto data to the CSV file
        for coin in coins_data:
            mkt_cap_fully_diluted = coin.get('fully_diluted_valuation', None)
            mkt_cap_to_fdv_ratio = None
            if mkt_cap_fully_diluted is not None:
                mkt_cap_to_fdv_ratio = coin['market_cap'] / mkt_cap_fully_diluted
            
            writer.writerow({
                'Coin': coin['name'],
                'Symbol': coin['symbol'].upper(),
                'Price': coin['current_price'],
                '1h': coin.get('price_change_percentage_1h_in_currency', None),
                '24h': coin.get('price_change_percentage_24h_in_currency', None),
                '7d': coin.get('price_change_percentage_7d_in_currency', None),
                '24h Volume': coin['total_volume'],
                'Mkt Cap': coin['market_cap'],
                'FDV': mkt_cap_fully_diluted,
                'Mkt Cap/FDV': mkt_cap_to_fdv_ratio
            })

# Check if the CSV file exists, and create it if it doesn't
if not os.path.exists(csv_file_path):
    with open(csv_file_path, mode='w', newline='') as file:
        pass

# Fetch top crypto data and save it to the CSV file
top_crypto_data = fetch_top_crypto_data()
save_data_to_csv(top_crypto_data)
