import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from streamlit_option_menu import option_menu

# Page configuration
st.set_page_config(
    page_title="EDGEVANTAGE",
    page_icon="https://raw.githubusercontent.com/4kMoose/EdgeVantage/main/EDGEVANTAGE%20-%20Logo_icon.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Basic page styling
st.markdown("""
    <style>
    .stApp {
        background-color: white;
    }
    .main-header {
        color: #00e900;
        font-family: 'Montserrat', sans-serif;
        font-weight: bold;
    }
    .stButton > button {
        background-color: #00e900;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 4px;
    }
    .stButton > button:hover {
        background-color: #00cc00;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    # Logo
    st.image("https://raw.githubusercontent.com/4kMoose/EdgeVantage/main/EDGEVANTAGE%20-%20Logotype.png", width=200)
    
    # Navigation
    selected = option_menu(
        menu_title=None,
        options=["Dashboard", "Strategy Builder", "Backtest", "Settings"],
        icons=["house", "gear", "graph-up", "sliders"],
        menu_icon=None,
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "white"},
            "icon": {"color": "#00e900", "font-size": "20px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "0px",
                "color": "#4d4d4d"
            },
            "nav-link-selected": {"background-color": "#00e900", "color": "white"},
        }
    )

# Banner under sidebar
st.image("https://raw.githubusercontent.com/4kMoose/EdgeVantage/main/EDGEVANTAGE%20-%20Layout.png", use_column_width=True)

# Strategy Components
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

# Moving Average Settings
st.subheader("Technical Indicators")
ma_enabled = st.checkbox("Enable Moving Average")
if ma_enabled:
    col1, col2 = st.columns(2)
    with col1:
        ma_period = st.number_input("MA Period", 5, 200, 14)
    with col2:
        ma_type = st.selectbox("MA Type", ["Simple", "Exponential"])

# Chart
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

# Backtest Results
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

# Footer
st.markdown("---")
st.markdown("EDGEVANTAGE v1.0 2024 | Powered by Advanced Trading Algorithms")
