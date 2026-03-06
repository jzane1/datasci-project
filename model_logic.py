import json
import requests
import pandas as pd

API_KEY = "n6te96qoYbPd2SSWic4sk6ymxcV9CEz98Xa4nN7b"
BASE_URL = "https://api.eia.gov/v2/electricity/rto/region-sub-ba-data/data/"


def fetch_ercot_data():
    """
    Fetches hourly demand by subregion for ERCOT (all of 2024)
    via the EIA v2 API. Paginates in batches of 5000 (API max).
    """
    all_rows = []
    offset = 0

    while True:
        x_params = {
            "frequency": "hourly",
            "data": ["value"],
            "facets": {"parent": ["ERCO"]},
            "start": "2023-06-01T00",
            "end": "2024-05-31T23",
            "sort": [{"column": "period", "direction": "asc"}],
            "offset": offset,
            "length": 5000
        }

        try:
            response = requests.get(
                BASE_URL,
                params={"api_key": API_KEY},
                headers={"X-Params": json.dumps(x_params)}
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data at offset {offset}: {e}")
            return None

        rows = response.json()["response"]["data"]
        if not rows:
            break

        all_rows.extend(rows)
        print(f"  Fetched {len(rows):,} rows (offset {offset:,})")

        if len(rows) < 5000:
            break
        offset += 5000

    df = pd.DataFrame(all_rows)
    df["period"] = pd.to_datetime(df["period"])
    df["value"] = pd.to_numeric(df["value"], errors="coerce")

    print(f"Total: {len(df):,} rows ({df['period'].min()} to {df['period'].max()})")
    return df

if __name__ == "__main__":
    ercot_df = fetch_ercot_data()
    if ercot_df is not None:
        pivot_df = ercot_df.pivot_table(
            index="period",
            columns="subba",
            values="value"
        ).sort_index()
        print(pivot_df.head(10))

        pivot_df.to_csv("ercot_demand.csv")
        print(f"\nSaved to ercot_demand.csv ({len(pivot_df)} rows)")



