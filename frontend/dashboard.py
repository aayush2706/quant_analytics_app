import streamlit as st
import time

from backend.state import ticks_df
from backend.resampling import resample
from backend.analytics import (
    compute_hedge_ratio,
    compute_zscore,
    compute_adf_pvalue,
    compute_rolling_correlation,
)
from backend.storage import persist


def render_dashboard():
    st.title("📈 Quant Real-Time Analytics Dashboard")

    st.metric("Ticks received", len(ticks_df))

    timeframe = st.selectbox("Timeframe", ["1S", "1min", "5min"])
    bars = resample(timeframe)

    if bars.empty:
        st.info("Waiting for bars...")
        st.write("Raw ticks:", len(ticks_df))
        return

    btc = bars[bars.symbol == "btcusdt"]["price"].reset_index(drop=True)
    eth = bars[bars.symbol == "ethusdt"]["price"].reset_index(drop=True)

    st.subheader("Latest Prices")
    c1, c2 = st.columns(2)
    if not btc.empty:
        c1.metric("BTCUSDT", round(btc.iloc[-1], 2))
    if not eth.empty:
        c2.metric("ETHUSDT", round(eth.iloc[-1], 2))

    st.subheader("Price Charts")
    c1, c2 = st.columns(2)
    if len(btc) > 10:
        c1.line_chart(btc)
    if len(eth) > 10:
        c2.line_chart(eth)

    if len(btc) < 5 or len(eth) < 5:
        st.info("Waiting for pair analytics...")
        return


    N = min(len(btc), len(eth))
    btc, eth = btc[-N:], eth[-N:]

    hedge = compute_hedge_ratio(btc, eth)
    spread = btc - hedge * eth
    z = compute_zscore(spread)
    corr = compute_rolling_correlation(btc, eth)

    z_threshold = st.slider("Z-score Alert Threshold", 0.5, 5.0, 2.0, 0.1)

    st.subheader("Pair Analytics")
    c1, c2, c3 = st.columns(3)
    c1.metric("Hedge Ratio", round(hedge, 4))
    c2.metric("Z-Score", round(z.iloc[-1], 2))
    c3.metric("ADF p-value", round(compute_adf_pvalue(spread), 4))

    if abs(z.iloc[-1]) > z_threshold:
        st.error("🚨 Z-Score Alert Triggered")

    st.subheader("Z-Score")
    st.line_chart(z)

    st.subheader("Rolling Correlation")
    st.line_chart(corr)

    st.subheader("Spread")
    st.line_chart(spread)

    csv = bars.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", csv, "processed_data.csv")

    if st.button("Save to Database"):
        persist(bars)
        st.success("Saved to market.db")
