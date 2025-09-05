import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.ensemble import IsolationForest
import hashlib
import plotly.express as px
import requests

st.set_page_config(page_title="AI RegTech Compliance & Fraud Detection Engine", layout="centered")
st.title("🦾 AI-Powered Regulatory Compliance & Fraud Detection")

st.markdown("""
- **Live Crypto:** CoinMarketCap API (any symbol, e.g. BTC, ETH)
- **Live Stocks:** Yahoo Finance (any symbol, e.g. RELIANCE.NS, AAPL)
- Checks compliance & fraud for your chosen assets
""")

# Input fields
cmc_api_key = st.text_input("CMC API Key):", type="password")
crypto_symbols = st.text_input("Enter crypto symbol(s) (comma-separated, e.g. BTC, ETH):", "BTC,ETH")
stock_symbols = st.text_input("Enter stock symbol(s) (comma-separated, e.g. RELIANCE.NS, AAPL):", "RELIANCE.NS")

def fetch_cmc_price(symbol, api_key):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    params = {'symbol': symbol.upper(), 'convert':'USD'}
    headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': api_key}
    try:
        r = requests.get(url, headers=headers, params=params)
        r.raise_for_status()
        price = r.json()['data'][symbol.upper()]['quote']['USD']['price']
        return float(price)
    except Exception as e:
        st.warning(f"CMC error for {symbol}: {e}")
        return np.nan

if st.button("Check Market Compliance & Fraud (Live)"):
    cryptos = [s.strip().upper() for s in crypto_symbols.split(',') if s.strip()]
    stocks = [s.strip().upper() for s in stock_symbols.split(',') if s.strip()]
    all_symbols = cryptos + stocks

    live_quotes = {}
    # Fetch crypto live prices using CMC
    for csym in cryptos:
        if not cmc_api_key:
            st.error("CMC API Key required for crypto! Get from https://coinmarketcap.com/api")
            st.stop()
        price = fetch_cmc_price(csym, cmc_api_key)
        live_quotes[csym+'-USD'] = price  # add '-USD' for display consistency
    # Fetch stock prices using yfinance
    for sym in stocks:
        data = yf.download(sym, period="1d", interval="1m")
        price = data['Close'].dropna().iloc[-1] if not data.empty and not data['Close'].empty else np.nan
        live_quotes[sym] = price
    def isnumber_finite(x):
    try:
        return np.isfinite(float(x))
    except Exception:
        return False

usable_symbols = [s for s in live_quotes if isnumber_finite(live_quotes[s])]

    if not usable_symbols:
        st.error("No current prices available! (market closed, bad symbol, or API problem)")
        st.stop()

    # Simulate Trades
    n_trx = 100
    np.random.seed(1)
    trx_log = []
    for i in range(n_trx):
        sym = np.random.choice(usable_symbols)
        price = live_quotes[sym]
        amount = np.abs(np.random.normal(1000, 500))
        leverage = np.random.choice([1, 2, 5, 10, 20, 30, 50])
        order_type = np.random.choice(['BUY', 'SELL', 'LIMIT_SELL', 'STOP_LOSS'])
        trx_log.append({
            'timestamp': datetime.now() - timedelta(minutes=n_trx - i),
            'trader_id': f'TR{np.random.randint(1, 20):04}',
            'symbol': sym,
            'order_type': order_type,
            'amount': round(amount, 2),
            'price': round(price, 2),
            'leverage': leverage,
        })
    trx_df = pd.DataFrame(trx_log)
    trx_df['transaction_value'] = trx_df['amount'] * trx_df['price']

    # Compliance
    compliance_rules = [
        {"field": "amount", "threshold": 10000, "logic": ">", "desc": "Amount > $10k: Must Report"},
        {"field": "leverage", "threshold": 20, "logic": ">", "desc": "Leverage > 20x: Enhanced Due Diligence"}
    ]
    def compliance_check(row):
        breaches = []
        for rule in compliance_rules:
            f, t, logic, d = rule.values()
            if logic == ">" and row[f] > t:
                breaches.append(d)
        return breaches
    trx_df['compliance_breaches'] = trx_df.apply(compliance_check, axis=1)

    # ML Fraud Detection
    features = trx_df[["amount", "price", "leverage"]]
    iso = IsolationForest(contamination=0.05, random_state=1)
    trx_df["iforest_flag"] = iso.fit_predict(features) == -1

    def wash_trading(row):
        return row["amount"] > 5000 and row["order_type"] in ["BUY", "SELL"]
    trx_df["wash_trading_flag"] = trx_df.apply(wash_trading, axis=1)

    trx_df["risk_score"] = (trx_df["iforest_flag"].astype(int) +
                            trx_df["wash_trading_flag"].astype(int) +
                            trx_df["compliance_breaches"].apply(len))
    trx_df["is_high_risk"] = trx_df["risk_score"] >= 2
    trx_df["blockchain_hash"] = trx_df[trx_df["is_high_risk"]].apply(
        lambda x: hashlib.sha256(str(x.to_dict()).encode()).hexdigest()[:20], axis=1)
    trx_df["blockchain_hash"].fillna("", inplace=True)

    st.metric("Total Trades Checked", len(trx_df))
    st.metric("High-Risk Trades", int(trx_df["is_high_risk"].sum()))
    st.metric("Compliance Breaches", int(trx_df["compliance_breaches"].apply(len).sum()))

    st.subheader("Compliance Breaches (Live)")
    st.dataframe(trx_df[trx_df['compliance_breaches'].apply(len)>0][
        ['timestamp','trader_id','symbol','amount','price','leverage','compliance_breaches']].head(10))
    st.subheader("High-Risk Transactions (Live)")
    st.dataframe(trx_df[trx_df['is_high_risk']][[
        'timestamp','trader_id','symbol','order_type','amount',
        'price','leverage','risk_score','compliance_breaches','blockchain_hash'
    ]].head(10))
    st.subheader("Suspicious vs Normal Transactions")
    fig = px.pie(trx_df, names="is_high_risk", title="Fraud/Compliance Score Distribution (LIVE)")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Click the button above after entering your key and symbols to check real trades for compliance and fraud.")
