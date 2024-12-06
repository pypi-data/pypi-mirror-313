import pandas as pd


def get_dates():
    return pd.date_range(start="2024-12-01", periods=10, freq="D")
