import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.ensemble import IsolationForest
import hashlib
import plotly.express as px
import requests

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
st.markdown(f"""
<style>
.bigfont {{
    font-size: 2.3rem !important;
    font-weight: 800;
    color: {primary};
    letter-spacing: -1px;
}}
.web3-gradient {{
    background: {web3_gradient};
    padding: 2.2rem 0;
    border-radius: 1.35rem;
    color: #fff;
    margin-bottom: 2rem;
}}
.warning {{
    background: {danger}; color:#fff; font-weight:900;
    padding:0.6em 1em; border-radius:0.7em; margin: 1em 0 0.5em 0
}}
.zn-box {{
    background: #383b5c22; border-radius: 1.2em; padding:1.5em; margin-bottom:1em;
}}
</style>
<div class='web3-gradient'>
<span class='bigfont'>finAIguard 🔮</span> — <span style='font-size:1.3em;'>Bridging Web3 🚀 & TradFi 🏦 with AI-powered Compliance & Fraud Detection</span><br>
<span style='color: #F9D923; font-size:1.08em;'>GenZ Ready. DeFi Native. Market Secure.</span>
</div>
""", unsafe_allow_html=True)

# Navigation & Intro
st.sidebar.header("✦ finAIguard – Settings")
cmc_api_key = st.sidebar.text_input("Your CoinMarketCap API Key", type="password")
crypto_symbols = st.sidebar.text_input("🪙 Crypto (comma-separated, e.g. BTC, ETH, DOGE)", "BTC,ETH")
stock_symbols = st.sidebar.text_input("📈 Stocks (comma-separated, e.g. RELIANCE.NS, AAPL)", "RELIANCE.NS")
n_trx = st.sidebar.slider("Simulation Trades (AI)", 100, 400, 100)

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
        st.warning(f"⚡️ CMC error for {symbol}: {e}")
        return np.nan

def isnumber_finite(x):
    try:
        return np.isfinite(float(x))
    except Exception:
        return False

st.markdown("## 💡 <b>How it works:</b>", unsafe_allow_html=True)
st.markdown(
    """
    1. 👾 Enter your crypto and/or stock symbols (any, as many as you like).
    2. 🤖 Click **Check Market Compliance & Fraud (Live)**.
    3. 🔳 Get instant dashboard + blockchain hashes for flagged trades.
    4. 🟦 **GenZ Tip:** Connect your web wallet to log flagged trades as POAP/Proof NFT (coming soon!).
    """
)

clicked = st.button("🧠 Check Market Compliance & Fraud (Live)")
if clicked:
    cryptos = [s.strip().upper() for s in crypto_symbols.split(',') if s.strip()]
    stocks = [s.strip().upper() for s in stock_symbols.split(',') if s.strip()]
    all_symbols = cryptos + stocks

    live_quotes = {}
    # Fetch crypto live prices using CMC
    for csym in cryptos:
        if not cmc_api_key:
            st.markdown(f"<div class='warning'>API Key required for {csym} from CoinMarketCap!</div>", unsafe_allow_html=True)
            st.stop()
        price = fetch_cmc_price(csym, cmc_api_key)
        live_quotes[f"{csym}-USD"] = price
    # Fetch stocks live prices using yfinance
    for sym in stocks:
        data = yf.download(sym, period="1d", interval="1m")
        price = data['Close'].dropna().iloc[-1] if not data.empty and not data['Close'].empty else np.nan
        live_quotes[sym] = price

    usable_symbols = [s for s in live_quotes if isnumber_finite(live_quotes[s])]
    if not usable_symbols:
        st.markdown(f"<div class='warning'>No valid symbols/data. Are markets open? Typo in names? API working?</div>", unsafe_allow_html=True)
        st.stop()

    def fmt_price(x):
    try:
        return f"{float(x):,.2f}"
    except Exception:
        return "N/A"

st.markdown(
    "<div class='zn-box' style='display:flex;flex-wrap:wrap;gap:1.1em;align-items:center;'>"
    "🌐 <b>Market prices loaded:</b> "
    + " ".join([
        f"<span style='display:inline-block;margin:0 0.8em 0 0;vertical-align:middle;font-size:1.10em;'><b>{s}</b> "
        + (f"<span style='color:{safe};font-weight:700;'>🟩 ${fmt_price(live_quotes[s])}</span>" if isnumber_finite(live_quotes[s]) else "<span style='color:red;font-weight:700;'>unavailable</span>")
        + "</span>"
        for s in usable_symbols
    ])
    + "</div>",
    unsafe_allow_html=True
)

    # Simulate Trades
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
            'trader_id': f'TR{np.random.randint(1, 30):04}',
            'symbol': sym,
            'order_type': order_type,
            'amount': round(amount, 2),
            'price': round(price, 2),
            'leverage': leverage,
        })
    trx_df = pd.DataFrame(trx_log)
    trx_df['transaction_value'] = trx_df['amount'] * trx_df['price']

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

    st.success("Fast AI check complete! Below is your Gen-Z proof-of-market-risk…")

    st.metric("Total Trades Checked", len(trx_df))
    st.metric("High-Risk Trades", int(trx_df["is_high_risk"].sum()))
    st.metric("Compliance Breaches", int(trx_df["compliance_breaches"].apply(len).sum()))

    st.markdown("### 🚨 Compliance Breaches (Live)")
    st.dataframe(trx_df[trx_df['compliance_breaches'].apply(len)>0][
        ['timestamp','trader_id','symbol','amount','price','leverage','compliance_breaches']].head(15), use_container_width=True)

    st.markdown("### ⛓️ High-Risk Transactions + OnChain Hash")
    st.dataframe(trx_df[trx_df['is_high_risk']][[
        'timestamp','trader_id','symbol','order_type','amount',
        'price','leverage','risk_score','compliance_breaches','blockchain_hash'
    ]].head(15), use_container_width=True)

    st.markdown("### 🟪 Suspicious vs Normal Transactions")
    fig = px.pie(trx_df, names="is_high_risk", title="Fraud/Compliance Score Distribution (LIVE)")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Set your symbols & Key and click the button for real-time Web3 risk/compliance.")

