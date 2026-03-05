import json
import requests
import pandas as pd

API_KEY = "n6te96qoYbPd2SSWic4sk6ymxcV9CEz98Xa4nN7b"
BASE_URL = "https://api.eia.gov/v2/electricity/rto/region-data/data/"

def fetch_ercot_data():
    """
    Fetches hourly demand, net generation, and solar/wind data for ERCOT
    via the EIA v2 API using the X-Params header.
    """
    x_params = {
        "frequency": "hourly",
        "data": ["value"],
        "facets": {
            "respondent": ["ERCO"]
        },
        "start": "2026-03-02T00",
        "end": None,
        "sort": [
            {"column": "period", "direction": "desc"}
        ],
        "offset": 0,
        "length": 5000
    }

    try:
        response = requests.get(
            BASE_URL,
            params={"api_key": API_KEY},
            headers={"X-Params": json.dumps(x_params)}
        )
        response.raise_for_status()
        data = response.json()

        df = pd.DataFrame(data["response"]["data"])
        df["period"] = pd.to_datetime(df["period"])

        print(f"Successfully loaded {len(df)} rows of data.")
        return df

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

if __name__ == "__main__":
    ercot_df = fetch_ercot_data()
    if ercot_df is not None:
        ercot_df["value"] = pd.to_numeric(ercot_df["value"], errors="coerce")
        pivot_df = ercot_df.pivot_table(
            index="period",
            columns="type",
            values="value"
        ).sort_index()
        print(pivot_df.head(20))
        

