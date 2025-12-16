import json
import threading
from websocket import WebSocketApp
import pandas as pd

from backend.state import ticks_df, lock

SYMBOLS = ["btcusdt", "ethusdt"]
_started = False


def on_message(ws, message):
    msg = json.loads(message)

    row = {
        "ts": pd.to_datetime(msg["T"], unit="ms"),
        "symbol": msg["s"].lower(),
        "price": float(msg["p"]),
    }

    with lock:
        ticks_df.loc[len(ticks_df)] = row


def start_socket(symbol):
    url = f"wss://fstream.binance.com/ws/{symbol}@trade"
    ws = WebSocketApp(url, on_message=on_message)
    ws.run_forever()


def start_ingestion():
    global _started
    if _started:
        return
    _started = True

    for sym in SYMBOLS:
        threading.Thread(
            target=start_socket,
            args=(sym,),
            daemon=True
        ).start()
