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
    
    # Technical Indicators
    st.subheader("Technical Indicators")
    
    # Moving Average
    st.markdown("### Moving Average")
    ma_enabled = st.checkbox("Enable Moving Average")
    if ma_enabled:
        ma_period = st.number_input("MA Period", 5, 200, 14)
        ma_type = st.selectbox("MA Type", ["Simple", "Exponential"])
    
    # RSI
    st.markdown("### RSI")
    rsi_enabled = st.checkbox("Enable RSI")
    if rsi_enabled:
        rsi_period = st.number_input("RSI Period", 5, 50, 14)
        rsi_overbought = st.number_input("Overbought Level", 50, 90, 70)
        rsi_oversold = st.number_input("Oversold Level", 10, 50, 30)
    
    # MACD
    st.markdown("### MACD")
    macd_enabled = st.checkbox("Enable MACD")
    if macd_enabled:
        macd_fast = st.number_input("Fast Period", 5, 50, 12)
        macd_slow = st.number_input("Slow Period", 10, 100, 26)
        macd_signal = st.number_input("Signal Period", 5, 50, 9)

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("Strategy Preview")
    
    # Generate sample data for visualization
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    prices = np.random.randn(len(dates)).cumsum() + 100
    
    # Create candlestick chart
    fig = go.Figure(data=[go.Candlestick(
        x=dates,
        open=prices + np.random.randn(len(dates)),
        high=prices + np.random.randn(len(dates)) + 1,
        low=prices + np.random.randn(len(dates)) - 1,
        close=prices + np.random.randn(len(dates))
    )])
    
    # Add indicators if enabled
    if ma_enabled:
        ma = pd.Series(prices).rolling(window=ma_period).mean()
        fig.add_trace(go.Scatter(x=dates, y=ma, name=f'{ma_period} MA'))
    
    fig.update_layout(
        title="Strategy Visualization",
        yaxis_title="Price",
        xaxis_title="Date"
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.header("Strategy Actions")
    
    # Entry Rules
    st.subheader("Entry Rules")
    entry_condition = st.selectbox(
        "Entry Condition",
        ["Price crosses above MA", "RSI below oversold", "MACD crossover"]
    )
    
    # Exit Rules
    st.subheader("Exit Rules")
    take_profit = st.number_input("Take Profit (pips)", 10, 1000, 100)
    stop_loss = st.number_input("Stop Loss (pips)", 10, 1000, 50)
    
    # Position Size
    st.subheader("Position Size")
    position_size = st.number_input("Position Size (lots)", 0.01, 10.0, 0.1)

# Backtest section
st.header("Backtest Results")
if st.button("Run Backtest"):
    with st.spinner("Running backtest..."):
        # Simulate backtest results
        st.success("Backtest completed!")
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Trades", "100")
        with col2:
            st.metric("Win Rate", "60%")
        with col3:
            st.metric("Profit Factor", "1.5")
        with col4:
            st.metric("Max Drawdown", "15%")
        
        # Sample equity curve
        equity_curve = np.random.randn(100).cumsum()
        st.line_chart(equity_curve)

# Deploy section
st.header("Deploy Strategy")
if st.button("Deploy to DBot"):
    # Add your deployment logic here
    st.success("Strategy deployed successfully! You can now use it in DBot.")
    st.info("Note: This is a demo version. Actual deployment requires Deriv API credentials.")
