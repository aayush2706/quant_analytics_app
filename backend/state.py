import pandas as pd
import threading

lock = threading.Lock()

ticks_df = pd.DataFrame(
    columns=["ts", "symbol", "price"]
)
