import streamlit as st
import yfinance as yf
import requests
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import hashlib

st.set_page_config(page_title="FinAIGuard - Indian Investor Dashboard", page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")

# Sidebar: Watchlist Section
st.sidebar.header("Your Watchlist (Moneycontrol Style)")
default_cryptos = st.sidebar.text_input("Cryptocurrency Watchlist (e.g. BTC, ETH)", value=st.session_state.get('watch_crypto', 'BTC,ETH'))
default_stocks = st.sidebar.text_input("Stock Watchlist (e.g. RELIANCE.NS, HDFCBANK.NS)", value=st.session_state.get('watch_stock', 'RELIANCE.NS,HDFCBANK.NS'))

# Persist user input for next use
st.session_state['watch_crypto'] = default_cryptos
st.session_state['watch_stock'] = default_stocks

api_key = st.sidebar.text_input("CoinMarketCap API Key", type="password")
st.sidebar.markdown("---")
n_transactions = st.sidebar.slider("Simulated Transactions", 100, 500, 100, help="For market risk simulation below.")
st.sidebar.markdown("---")
st.sidebar.info("Note: Ensure all accounts and trades comply with SEBI and RBI norms for Indian investors. Crypto taxation (flat 30%) and reporting is compulsory as per 2022 regulations.", icon="📢")

def fetch_crypto_quotes(symbols, api_key):
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    headers = {"Accepts": "application/json", "X-CMC_PRO_API_KEY": api_key}
    params = {"symbol": ','.join(symbols), "convert": "INR"}
    results = {}
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=10)
        for s in symbols:
            d = resp.json()["data"].get(s.upper())
            if d:
                q = d["quote"]["INR"]
                results[s] = {
                    "price": q["price"],
                    "change_pct": q["percent_change_24h"]
                }
    except Exception as e:
        pass
    return results

def fetch_stock_quotes(symbols):
    results = {}
    for s in symbols:
        try:
            df = yf.download(s, period="2d", interval="1d")
            if df.shape[0] > 1:
                last = df.iloc[-1]
                prev = df.iloc[-2]
                price = float(last["Close"])
                pchg = ((price - float(prev["Close"])) / float(prev["Close"])) * 100
                results[s] = {
                    "price": price,
                    "change_pct": pchg
                }
        except Exception:
            continue
    return results

# --- WATCHLIST DASHBOARD ---
st.header("Watchlist - Live Market Overview")
crypto_syms = [x.strip().upper() for x in default_cryptos.split(",") if x.strip()]
stock_syms = [x.strip().upper() for x in default_stocks.split(",") if x.strip()]

crypto_quotes = fetch_crypto_quotes(crypto_syms, api_key) if api_key else {}
stock_quotes = fetch_stock_quotes(stock_syms)

def format_inr(val):
    return "₹{:,.2f}".format(val)

watchlist_rows = []
for s in crypto_syms:
    data = crypto_quotes.get(s)
    if data:
        change_col = f":green[{data['change_pct']:+.2f}%]" if data["change_pct"] >= 0 else f":red[{data['change_pct']:+.2f}%]"
        watchlist_rows.append({
            "Symbol": s,
            "Price": format_inr(data["price"]),
            "24H Change": change_col
        })
    else:
        watchlist_rows.append({"Symbol": s, "Price": "N/A", "24H Change": "-"})

for s in stock_syms:
    data = stock_quotes.get(s)
    if data:
        change_col = f":green[{data['change_pct']:+.2f}%]" if data["change_pct"] >= 0 else f":red[{data['change_pct']:+.2f}%]"
        watchlist_rows.append({
            "Symbol": s,
            "Price": format_inr(data["price"]),
            "1D Change": change_col
        })
    else:
        watchlist_rows.append({"Symbol": s, "Price": "N/A", "1D Change": "-"})

if watchlist_rows:
    st.dataframe(pd.DataFrame(watchlist_rows).fillna(""), use_container_width=True)

refresh = st.button("🔄 Refresh Watchlist Prices")
if refresh:
    st.experimental_rerun()

# --- ANALYSIS SECTION ---
st.subheader("Market Analysis & Compliance Check")
# ... keep your transaction simulation/compliance monitoring/DF sections as before!
