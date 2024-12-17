import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="EDGEVANTAGE",
    page_icon="https://raw.githubusercontent.com/4kMoose/EdgeVantage/main/EDGEVANTAGE%20-%20Logo_icon.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide sidebar and menu
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    .css-1rs6os {visibility: hidden;}
    .css-17ziqus {visibility: hidden;}
    .css-1dp5vir {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Banner at the top
st.markdown('<div class="banner-container">', unsafe_allow_html=True)
st.image("https://raw.githubusercontent.com/4kMoose/EdgeVantage/main/EDGEVANTAGE%20-%20Banner.png", use_column_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Main content
st.markdown("""
    <div class="main-content">
        <h2 class="montserrat-heading">Strategy Builder</h2>
    </div>
""", unsafe_allow_html=True)

# Strategy Components in a modern card layout
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("Strategy Components")
col1, col2, col3 = st.columns(3)

with col1:
    risk_tolerance = st.slider("Risk Tolerance", 1, 10, 5)
with col2:
    trading_session = st.selectbox(
        "Trading Session",
        ["Asian", "European", "American"]
    )
with col3:
    asset_class = st.selectbox(
        "Asset Class",
        ["Forex", "Crypto", "Commodities"]
    )
st.markdown('</div>', unsafe_allow_html=True)

# Technical Indicators
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("Technical Indicators")
ma_enabled = st.checkbox("Enable Moving Average")
if ma_enabled:
    col1, col2 = st.columns(2)
    with col1:
        ma_period = st.number_input("MA Period", 5, 200, 14)
    with col2:
        ma_type = st.selectbox("MA Type", ["Simple", "Exponential"])
st.markdown('</div>', unsafe_allow_html=True)

# Chart
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("Strategy Preview")
dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
prices = 100 + np.random.randn(100).cumsum()

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=dates,
    y=prices,
    name='Price',
    line=dict(color='#00e900', width=2)
))

if ma_enabled:
    ma = pd.Series(prices).rolling(window=ma_period).mean()
    fig.add_trace(go.Scatter(
        x=dates,
        y=ma,
        name=f'{ma_period} MA',
        line=dict(color='#4d4d4d', width=2)
    ))

fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    yaxis_title="Price",
    xaxis_title="Date",
    height=500,
    showlegend=True
)

st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Settings Section
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("Settings")
col1, col2 = st.columns(2)
with col1:
    st.selectbox("Theme", ["Light", "Dark"])
    st.selectbox("Chart Style", ["Modern", "Classic"])
with col2:
    st.selectbox("Time Zone", ["UTC", "Local"])
    st.selectbox("Currency", ["USD", "EUR", "GBP"])
st.markdown('</div>', unsafe_allow_html=True)

# Backtest Results
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("Backtest Results")
if st.button("Run Backtest"):
    with st.spinner("Running backtest..."):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Trades", "50", delta="↑")
        with col2:
            st.metric("Win Rate", "60%", delta="↑ 5%")
        with col3:
            st.metric("Profit Factor", "1.5", delta="↑ 0.2")
        with col4:
            st.metric("Max Drawdown", "15%", delta="↓ 3%")
        
        equity = 1000 * (1 + np.random.randn(50).cumsum() * 0.02)
        equity_fig = go.Figure()
        equity_fig.add_trace(go.Scatter(
            y=equity,
            mode='lines',
            name='Equity Curve',
            line=dict(color='#00e900', width=2)
        ))
        equity_fig.update_layout(
            title="Equity Curve",
            yaxis_title="Equity ($)",
            xaxis_title="Trade Number",
            height=300,
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        st.plotly_chart(equity_fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class="footer">
        <p class="montserrat-footer">EDGEVANTAGE v1.0 2024 | Powered by Advanced Trading Algorithms</p>
    </div>
""", unsafe_allow_html=True)
