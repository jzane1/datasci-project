import requests
import pandas as pd
import os

# API Configuration
API_KEY = "n6te96qoYbPd2SSWic4sk6ymxcV9CEz98Xa4nN7b"
BASE_URL = "https://api.eia.gov/v2/electricity/rto/region-data/data/"

def fetch_ercot_data():
    """
    Fetches hourly demand, net generation, and solar/wind data for ERCOT.
    """
    # Parameters for the EIA v2 API
    params = {
        'api_key': API_KEY,
        'frequency': 'hourly',
        'data[0]': 'value',
        'facets[respondent][]': 'ERCO',  # ERCOT Regional Transmission Org
        'sort[0][column]': 'period',
        'sort[0][direction]': 'desc',
        'offset': 0,
        'length': 5000 # Adjust based on how much history you want for the baseline
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Extract observations
        df = pd.DataFrame(data['response']['data'])
        
        # Convert period to datetime
        df['period'] = pd.to_datetime(df['period'])
        
        print(f"Successfully loaded {len(df)} rows of data.")
        return df
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

if __name__ == "__main__":
        # Test the pull
    ercot_df = fetch_ercot_data()
    if ercot_df is not None:
        # Pivot the data so each timestamp is one row with columns for D, DF, NG, TI
        pivot_df = ercot_df.pivot_table(
            index='period', 
            columns='type', 
            values='value'
        ).sort_index()
        print(pivot_df.head())

