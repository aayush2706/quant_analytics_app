import pandas as pd
from backend.state import ticks_df, lock


def resample(freq: str) -> pd.DataFrame:
    with lock:
        if ticks_df.empty:
            return pd.DataFrame()

        df = ticks_df.copy()

    df = df.set_index("ts")

    bars = (
        df
        .groupby("symbol")
        .resample(freq)["price"]
        .last()
        .unstack("symbol")        # <-- KEY FIX
        .dropna()                 # <-- ensure both BTC & ETH exist
        .stack()
        .reset_index(name="price")
    )

    return bars
