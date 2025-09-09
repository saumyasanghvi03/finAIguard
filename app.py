import streamlit as st
import yfinance as yf
import requests
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import hashlib

st.set_page_config(page_title="FinAIGuard - Market Compliance & Fraud Detection", page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")

def fetch_crypto_prices(symbols, api_key):
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    headers = {"Accepts": "application/json", "X-CMC_PRO_API_KEY": api_key}
    params = {"symbol": ','.join(symbols), "convert": "USD"}
    prices = {}
    errors = []
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=12)
        data = resp.json().get("data", {})
        for s in symbols:
            entry = data.get(s.upper())
            if entry:
                prices[s.upper()] = float(entry["quote"]["USD"]["price"])
            else:
                errors.append(s.upper())
    except Exception as e:
        st.warning(f"CoinMarketCap error: {e}")
        errors.extend(symbols)
    return prices, errors

def fetch_stock_prices(symbols):
    prices = {}
    errors = []
    for s in symbols:
        try:
            df = yf.download(s, period="1d", interval="1m")
            price = float(df["Close"].dropna().iloc[-1]) if not df.empty else None
            if price:
                prices[s.upper()] = price
            else:
                errors.append(s.upper())
        except Exception:
            errors.append(s.upper())
    return prices, errors

st.sidebar.header("Configuration Settings")
api_key = st.sidebar.text_input("CoinMarketCap API Key", type="password")
crypto_input = st.sidebar.text_input("Cryptocurrency Symbols (comma-separated, e.g. BTC, ETH)", "BTC,ETH")
stock_input = st.sidebar.text_input("Stock Symbols (comma-separated, e.g. RELIANCE.NS, AAPL)", "AAPL,RELIANCE.NS")
n_transactions = st.sidebar.slider("Simulated Transactions", 100, 500, 100)

st.title("finAIguard")
st.markdown("Advanced Market Compliance & Fraud Detection Analytics")
st.subheader("Market Analysis & Compliance Check")

if st.button("Check Market Compliance & Fraud (Live)"):
    st.info("Fetching live market data and simulating transactions...")
    crypto_syms = [x.strip().upper() for x in crypto_input.split(",") if x.strip()]
    stock_syms = [x.strip().upper() for x in stock_input.split(",") if x.strip()]

    prices, errors = {}, []
    crypto_prices, crypto_errors = fetch_crypto_prices(crypto_syms, api_key) if api_key and crypto_syms else ({}, crypto_syms)
    stock_prices, stock_errors = fetch_stock_prices(stock_syms) if stock_syms else ({}, stock_syms)
    prices.update(crypto_prices)
    prices.update(stock_prices)
    errors.extend(crypto_errors + stock_errors)

    st.markdown("**Live Crypto Prices:**")
    for s in crypto_syms:
        if s in crypto_prices:
            st.write(f"{s}: ${crypto_prices[s]:,.2f}")
        else:
            st.warning(f"No price for {s}")

    st.markdown("**Live Stock Prices:**")
    for s in stock_syms:
        if s in stock_prices:
            st.write(f"{s}: ${stock_prices[s]:,.2f}")
        else:
            st.warning(f"No price for {s}")

    if not prices:
        st.error("No valid prices: please check your API key and symbols.")
    else:
        now = datetime.now()
        tx_data = []
        all_syms = list(prices.keys())
        for i in range(n_transactions):
            symbol = np.random.choice(all_syms)
            price = prices[symbol]
            amount = float(np.abs(np.random.normal(1000, 250)))
            order_type = np.random.choice(['BUY', 'SELL', 'LIMIT_SELL', 'STOP_LOSS'])
            leverage = np.random.choice([1, 2, 5, 10, 20])
            value = round(amount * price, 2)
            compliance_breach = value > 10000 or leverage > 10
            fraud_flag = order_type in ["LIMIT_SELL", "STOP_LOSS"] and value > 15000
            risk_score = int(compliance_breach) + int(fraud_flag)
            timestamp = now - timedelta(minutes=n_transactions - i)
            hash_val = hashlib.sha256(str({
                "symbol": symbol,
                "price": price,
                "amount": amount,
                "time": timestamp.isoformat()
            }).encode()).hexdigest()[:12] if risk_score >= 2 else ""
            tx_data.append({
                "timestamp": timestamp,
                "symbol": symbol,
                "order_type": order_type,
                "amount": round(amount, 2),
                "price": round(price, 2),
                "leverage": leverage,
                "value": value,
                "compliance_breach": compliance_breach,
                "fraud_flag": fraud_flag,
                "risk_score": risk_score,
                "hash": hash_val
            })
        df = pd.DataFrame(tx_data)
        st.metric("Total Transactions Checked", len(df))
        st.metric("Compliance Breaches", int(df['compliance_breach'].sum()))
        st.metric("High-Risk Transactions", int((df['risk_score'] >= 2).sum()))
        st.markdown("### Recent Transactions (top 15)")
        st.dataframe(df.head(15))

        st.subheader("Transaction Monitoring")
        st.write("Real-time transaction monitoring and anomaly detection capabilities.")

        st.subheader("Regulatory Compliance")
        st.write("Automated compliance checking against financial regulations and standards.")
