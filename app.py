import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.ensemble import IsolationForest
import hashlib
import plotly.express as px
import requests

# Add CSS styling at the top of the app
st.markdown("""
<style>
.bigfont {
    font-size: 2.3rem !important;
    font-weight: 800;
    color: #8323FF;
    letter-spacing: -1px;
}
.web3-gradient {
    background: linear-gradient(90deg, #8323FF 0%, #23FFE6 100%);
    padding: 2.2rem 0;
    border-radius: 1.35rem;
    text-align: center;
    margin-bottom: 2rem;
}
.zn-box {
    background: rgba(131, 35, 255, 0.1);
    border: 2px solid #8323FF;
    border-radius: 1rem;
    padding: 1.5rem;
    margin: 1rem 0;
    backdrop-filter: blur(10px);
}
.info-bar {
    background: linear-gradient(135deg, #5CFFC9 0%, #23FFE6 100%);
    color: #1e1e1e;
    padding: 1rem;
    border-radius: 0.75rem;
    font-weight: 600;
    text-align: center;
    margin: 1rem 0;
    box-shadow: 0 4px 15px rgba(92, 255, 201, 0.3);
}
</style>
""", unsafe_allow_html=True)

# GENZ COLORS + EMOJIS
primary = "#8323FF"
escrow = "#F9D923"
safe = "#5CFFC9"
danger = "#FF3B3B"
web3_gradient = "linear-gradient(90deg, #8323FF 0%, #23FFE6 100%)"

st.set_page_config(
    page_title="finAIguard: Web3 Compliance/Fraud Engine",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Web3 Banner
st.markdown(
f""".bigfont {{
    font-size: 2.3rem !important;
    font-weight: 800;
    color: {primary};
    letter-spacing: -1px;
}}
.web3-gradient {{
    background: {web3_gradient};
    padding: 2.2rem 0;
    border-radius: 1.35rem;
