import os
import pandas as pd
from fredapi import Fred
from dotenv import load_dotenv

load_dotenv('/app/.env')

def get_fred_client():
    api_key = os.getenv('FRED_API_KEY')
    if not api_key:
        raise ValueError("FRED_API_KEY not found in .env")
    return Fred(api_key=api_key)

def fetch_series(fred, series_id, name):
    print(f"Fetching {name}...")
    data = fred.get_series(series_id)
    data.name = name
    return data

def load_all():
    fred = get_fred_client()
    
    inr   = fetch_series(fred, 'DEXINUS',      'INR_USD')
    brent = fetch_series(fred, 'DCOILBRENTEU', 'BRENT')
    forex = fetch_series(fred, 'TRESEGINM052N',        'INDIA_FOREX_RESERVES')
    fed   = fetch_series(fred, 'FEDFUNDS',      'FED_FUNDS_RATE')
    
    df = pd.concat([inr, brent, forex, fed], axis=1)
    df.index.name = 'date'
    df = df.sort_index()
    
    os.makedirs('/app/data/raw', exist_ok=True)
    df.to_csv('/app/data/raw/macro_data.csv')
    print(f"Saved to data/raw/macro_data.csv — shape: {df.shape}")
    
    return df

if __name__ == '__main__':
    df = load_all()
    print(df.tail())
