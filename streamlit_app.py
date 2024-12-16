import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from streamlit_option_menu import option_menu

# Load custom CSS
with open('assets/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Hide Streamlit's default menu and footer
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    /* Import Font Awesome */
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css');
    </style>
""", unsafe_allow_html=True)

# Page configuration
st.set_page_config(
    page_title="EDGEVANTAGE",
    page_icon="https://raw.githubusercontent.com/4kMoose/EdgeVantage/main/EDGEVANTAGE%20-%20Logo_icon.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar navigation
with st.sidebar:
    # Center the logo in the sidebar
    col1, col2, col3 = st.columns([1,3,1])
    with col2:
        st.image("https://raw.githubusercontent.com/4kMoose/EdgeVantage/main/EDGEVANTAGE%20-%20Logotype.png", width=150)
    
    st.markdown("<br>", unsafe_allow_html=True)  # Add some spacing
    
    selected = option_menu(
        menu_title=None,
        options=["Dashboard", "Strategy Builder", "Backtest", "Settings"],
        icons=["house", "gear", "graph-up", "sliders"],
        menu_icon=None,
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#000000"},
            "icon": {"color": "#00e900", "font-size": "20px"}, 
            "nav-link": {
                "font-size": "16px", 
                "text-align": "left", 
                "margin":"0px", 
                "--hover-color": "#4d4d4d",
                "font-family": "Montserrat"
            },
            "nav-link-selected": {"background-color": "#00e900"},
        }
    )

# Main content area
container = st.container()
with container:
    # Banner with adjusted padding
    st.markdown('<div style="padding: 0 5%;">', unsafe_allow_html=True)
    st.image("https://raw.githubusercontent.com/4kMoose/EdgeVantage/main/EDGEVANTAGE%20-%20Layout.png", use_column_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Add some spacing
    st.markdown("<br>", unsafe_allow_html=True)

    # Strategy Components in a card with adjusted padding
    st.markdown("""
        <div style="padding: 0 5%;">
            <div class="custom-card">
                <h3><i class="fas fa-cogs"></i> Strategy Components</h3>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Components in columns with padding
    with st.container():
        st.markdown('<div style="padding: 0 5%;">', unsafe_allow_html=True)
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
    st.markdown("""
        <div style="padding: 0 5%;">
            <div class="custom-card">
                <h3><i class="fas fa-chart-line"></i> Technical Indicators</h3>
            </div>
        </div>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div style="padding: 0 5%;">', unsafe_allow_html=True)
        ma_enabled = st.checkbox("Enable Moving Average")
        if ma_enabled:
            col1, col2 = st.columns(2)
            with col1:
                ma_period = st.number_input("MA Period", 5, 200, 14)
            with col2:
                ma_type = st.selectbox("MA Type", ["Simple", "Exponential"])
        st.markdown('</div>', unsafe_allow_html=True)

    # Chart Section
    st.markdown("""
        <div style="padding: 0 5%;">
            <div class="custom-card">
                <h3><i class="fas fa-chart-area"></i> Strategy Preview</h3>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Generate sample data and create chart
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
        title=None,  # Remove title for cleaner look
        yaxis_title="Price",
        xaxis_title="Date",
        height=400,
        font=dict(family="Montserrat"),
        showlegend=True,
        margin=dict(l=40, r=40, t=40, b=40),  # Adjust margins
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor="rgba(255, 255, 255, 0.8)"
        )
    )

    st.markdown('<div style="padding: 0 5%;">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Backtest Results
    st.markdown("""
        <div style="padding: 0 5%;">
            <div class="custom-card">
                <h3><i class="fas fa-calculator"></i> Backtest Results</h3>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="padding: 0 5%;">', unsafe_allow_html=True)
    if st.button("Run Backtest", type="primary"):  # Make button more prominent
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
                title=None,
                yaxis_title="Equity ($)",
                xaxis_title="Trade Number",
                height=300,
                font=dict(family="Montserrat"),
                plot_bgcolor='white',
                paper_bgcolor='white',
                margin=dict(l=40, r=40, t=40, b=40),
                showlegend=False
            )
            st.plotly_chart(equity_fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Custom footer
st.markdown("""
    <div class="footer" style="padding: 1rem 5%; text-align: center; color: #4d4d4d; font-family: Montserrat;">
        <p>EDGEVANTAGE v1.0 2024 | Powered by Advanced Trading Algorithms</p>
    </div>
    """, unsafe_allow_html=True)
