import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Initialize session state
if 'strategy_count' not in st.session_state:
    st.session_state.strategy_count = 0

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
    np.random.seed(42)  # For reproducible results
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    base_price = 100
    noise = np.random.normal(0, 1, len(dates))
    trend = np.linspace(0, 10, len(dates))
    prices = base_price + trend + noise.cumsum()
    
    # Create candlestick data
    opens = prices + np.random.normal(0, 0.5, len(dates))
    highs = np.maximum(opens, prices) + np.random.uniform(0, 1, len(dates))
    lows = np.minimum(opens, prices) - np.random.uniform(0, 1, len(dates))
    closes = prices + np.random.normal(0, 0.5, len(dates))
    
    # Create candlestick chart
    fig = go.Figure(data=[go.Candlestick(
        x=dates,
        open=opens,
        high=highs,
        low=lows,
        close=closes
    )])
    
    # Add indicators if enabled
    if ma_enabled:
        ma = pd.Series(closes).rolling(window=ma_period).mean()
        fig.add_trace(go.Scatter(x=dates, y=ma, name=f'{ma_period} MA', line=dict(color='blue')))
    
    if rsi_enabled:
        # Simple RSI calculation for demo
        delta = pd.Series(closes).diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=rsi_period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=rsi_period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        # Add RSI in a subplot
        fig.add_trace(go.Scatter(x=dates, y=rsi, name='RSI', yaxis="y2"))
        fig.update_layout(
            yaxis2=dict(
                title="RSI",
                overlaying="y",
                side="right",
                range=[0, 100]
            )
        )
    
    fig.update_layout(
        title="Strategy Visualization",
        yaxis_title="Price",
        xaxis_title="Date",
        height=600
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
        st.session_state.strategy_count += 1
        
        # Generate random but realistic-looking backtest results
        total_trades = np.random.randint(50, 150)
        win_rate = np.random.uniform(0.4, 0.7)
        profit_factor = np.random.uniform(1.1, 2.0)
        max_drawdown = np.random.uniform(0.1, 0.3)
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Trades", f"{total_trades}")
        with col2:
            st.metric("Win Rate", f"{win_rate:.1%}")
        with col3:
            st.metric("Profit Factor", f"{profit_factor:.2f}")
        with col4:
            st.metric("Max Drawdown", f"{max_drawdown:.1%}")
        
        # Generate equity curve
        trades = np.random.normal(0.002, 0.005, total_trades)
        equity_curve = (1 + trades).cumprod()
        
        # Plot equity curve
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            y=equity_curve,
            mode='lines',
            name='Equity Curve',
            line=dict(color='green')
        ))
        fig.update_layout(
            title="Equity Curve",
            yaxis_title="Equity Growth",
            xaxis_title="Trade Number",
            showlegend=True
        )
        st.plotly_chart(fig, use_container_width=True)

# Deploy section
st.header("Deploy Strategy")
if st.button("Deploy to DBot"):
    # Simulated deployment
    with st.spinner("Deploying strategy..."):
        st.success("Strategy deployed successfully! You can now use it in DBot.")
        st.info("""
        Note: This is a demo version. In the full version, this would:
        1. Connect to your Deriv account
        2. Upload the strategy to DBot
        3. Start automated trading
        """)

# Add a footer with version info
st.markdown("---")
st.markdown("DBot Strategy Generator v1.0 - Demo Version")
