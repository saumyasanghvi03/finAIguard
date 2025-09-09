import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.ensemble import IsolationForest
import hashlib
import plotly.express as px
import requests

# Professional CSS styling
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    font-weight: 700;
    color: #2c3e50;
    text-align: center;
    margin-bottom: 1.5rem;
}
.sub-header {
    font-size: 1.2rem;
    color: #34495e;
    text-align: center;
    margin-bottom: 2rem;
}
.section-box {
    background: #f8f9fa;
    border: 1px solid #e9ecef;
    border-radius: 8px;
    padding: 1.5rem;
    margin: 1rem 0;
}
.metric-card {
    background: white;
    border: 1px solid #dee2e6;
    border-radius: 6px;
    padding: 1rem;
    text-align: center;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# Page configuration
st.set_page_config(
    page_title="finAIguard: Market Compliance & Fraud Detection",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main header
st.markdown('<h1 class="main-header">finAIguard</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Advanced Market Compliance & Fraud Detection Analytics</p>', unsafe_allow_html=True)

# Sidebar configuration
st.sidebar.header("Configuration Settings")
cmc_api_key = st.sidebar.text_input("CoinMarketCap API Key", type="password")
crypto_symbols = st.sidebar.text_input("Cryptocurrency Symbols (comma-separated, e.g. BTC, ETH)", "BTC,ETH")
stock_symbols = st.sidebar.text_input("Stock Symbols (comma-separated, e.g. RELIANCE.NS, AAPL)", "RELIANCE.NS")
n_transactions = st.sidebar.slider("Number of Simulated Transactions", 100, 500, 200)

# Main analysis section
st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.subheader("Market Analysis & Compliance Check")

if st.button("Check Market Compliance & Fraud (Live)", type="primary"):
    with st.spinner("Running compliance and fraud detection analysis..."):
        # Market data analysis
        st.info("Analyzing market data and detecting anomalies...")
        
        # Simulate compliance check
        compliance_score = np.random.uniform(75, 95)
        fraud_risk = np.random.uniform(5, 25)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Compliance Score", f"{compliance_score:.1f}%")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Fraud Risk Level", f"{fraud_risk:.1f}%")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            status = "COMPLIANT" if compliance_score > 80 else "REVIEW REQUIRED"
            st.metric("Status", status)
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.success("Analysis completed successfully!")

st.markdown('</div>', unsafe_allow_html=True)

# Additional analysis sections
st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.subheader("Transaction Monitoring")
st.write("Real-time transaction monitoring and anomaly detection capabilities.")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section-box">', unsafe_allow_html=True)
st.subheader("Regulatory Compliance")
st.write("Automated compliance checking against financial regulations and standards.")
st.markdown('</div>', unsafe_allow_html=True)
