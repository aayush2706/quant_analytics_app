from backend.ingestion import start_ingestion
from frontend.dashboard import render_dashboard

# Start WebSocket ingestion exactly once
start_ingestion()

# Render Streamlit dashboard
render_dashboard()
