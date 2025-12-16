Quant Real-Time Analytics Dashboard

Overview:
This project is a real-time market data analytics dashboard built using live Binance Futures trade data.
It ingests tick-level data, resamples it into OHLC bars, performs basic quantitative pair analytics, and visualizes the results in a Streamlit dashboard.
The focus of this assignment is data ingestion, resampling, analytics correctness, and system structure, rather than UI polish.

Features Implemented:
Live Market Data Ingestion
Binance Futures WebSocket trade stream
Symbols: BTCUSDT, ETHUSDT
Threaded ingestion for non-blocking updates
In-memory storage for real-time access

Supported timeframes:
1 second
1 minute
5 minutes
Symbol-wise aggregation

Analytics:
Hedge ratio estimation using OLS regression
Spread calculation between BTC and ETH
Z-score computation on spread
Augmented Dickey-Fuller (ADF) p-value
Rolling correlation
Z-score threshold alert

Dashboard:
Live tick counter
Timeframe selector
Latest prices
Price charts
Spread, Z-score, and correlation charts
CSV download of processed bars
Save processed data to SQLite database

Storage:
In-memory state for live processing
SQLite database (market.db) for persistence

Project Structure
quant_analytics_app/
├── app.py
├── backend/
│   ├── ingestion.py
│   ├── state.py
│   ├── resampling.py
│   ├── analytics.py
│   └── storage.py
├── frontend/
│   └── dashboard.py
├── market.db
├── requirements.txt
└── README.md

How to Run
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py


The app will be available at:
(http://192.168.29.79:8501)

Notes:
Analytics are computed only after sufficient data is available
Edge cases (empty data, short windows) are handled safely
FutureWarnings shown in terminal are from pandas/statsmodels and do not affect correctness

ChatGPT Usage:
ChatGPT was used as a development assistant for debugging, code refinement, and validation.
All code was run, tested, and verified locally.

Summary:
This project demonstrates:
Real-time data ingestion
Proper market data resampling
Core quantitative analytics
Clear backend/frontend separation
