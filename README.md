# ERCOT Load Forecasting: COAST Zone Analysis

Energy supply in Texas is operated by the Electric Reliability Council of Texas (ERCOT). ERCOT continually generates short-term energy demand forecasts to ensure:
* **Grid reliability**
* **Effective renewables integration**
* **Operational cost minimization**

Forecasting errors can have severe short-term consequences (as seen in February 2021) and accumulate significant long-term financial losses. 

### Project Aim
Our aim is to develop a machine learning model that outperforms ERCOT’s proprietary neural-network-based model. We consider energy demand in Texas’ **COAST (COAS) zone**, using data from **June 1, 2023, to May 31, 2024**.

All work, feature engineering, and performance analysis are documented in [notebook.ipynb](./notebook.ipynb). 

---

### Data Access & Reproducibility
Due to file size limits and API restrictions, data is handled as follows:

1. **Actual Electricity Demand:** This data was obtained via the EIA (U.S. Energy Information Administration) API. To reproduce the results, please register for a personal API key on the [EIA website](https://www.eia.gov/opendata/register.php) and input it into the designated cell in the notebook.
2. **ERCOT Forecast Data:** The historical forecast comparison data is too large to be hosted directly in this repository. The full dataset can be found [here](https://drive.google.com/file/d/1BwlBYQWykMGakHJmeqzi4_lpbZGAY_To/view).

---

### Key Findings
* **Model Used:** XGBoost (Gradient Boosted Decision Trees)
* **Target Metric:** Mean Absolute Error (MAE)
* **Primary Drivers:** Temperature, Dew Point, and Lagged Load Demand
