import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="DBot Strategy Generator",
    page_icon="📈",
    layout="wide"
)

# Title and description
st.title("DBot Strategy Generator")
st.markdown("Create and backtest your trading strategies with ease!")

# Sidebar for strategy components
with st.sidebar:
    st.header("Strategy Components")
    
    # Strategy Settings
    st.subheader("General Settings")
    risk_tolerance = st.slider("Risk Tolerance", 1, 10, 5)
    trading_session = st.selectbox(
        "Trading Session",
        ["Asian", "European", "American"]
    )
    asset_class = st.selectbox(
        "Asset Class",
        ["Forex", "Crypto", "Commodities"]
    )
    
    # Moving Average
    st.subheader("Moving Average")
    ma_enabled = st.checkbox("Enable Moving Average")
    if ma_enabled:
        ma_period = st.number_input("MA Period", 5, 200, 14)
        ma_type = st.selectbox("MA Type", ["Simple", "Exponential"])

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("Strategy Preview")
    
    # Generate sample data
    dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
    prices = 100 + np.random.randn(100).cumsum()
    
    # Create basic line chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=prices, name='Price'))
    
    if ma_enabled:
        ma = pd.Series(prices).rolling(window=ma_period).mean()
        fig.add_trace(go.Scatter(x=dates, y=ma, name=f'{ma_period} MA'))
    
    fig.update_layout(
        title="Price Chart",
        yaxis_title="Price",
        xaxis_title="Date",
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.header("Strategy Actions")
    
    # Entry Rules
    st.subheader("Entry Rules")
    entry_condition = st.selectbox(
        "Entry Condition",
        ["Price crosses above MA", "Price crosses below MA"]
    )
    
    # Position Size
    st.subheader("Position Size")
    position_size = st.number_input("Position Size (lots)", 0.01, 10.0, 0.1)

# Backtest section
st.header("Backtest Results")
if st.button("Run Backtest"):
    with st.spinner("Running backtest..."):
        # Display sample metrics
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Trades", "50")
            st.metric("Win Rate", "60%")
        with col2:
            st.metric("Profit Factor", "1.5")
            st.metric("Max Drawdown", "15%")
        
        # Sample equity curve
        equity = 1000 * (1 + np.random.randn(50).cumsum() * 0.02)
        st.line_chart(equity)

st.markdown("---")
st.markdown("DBot Strategy Generator v1.0 - Demo Version")
