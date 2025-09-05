import streamlit as st
import pandas as pd
import numpy as np
import requests
from datetime import datetime
import hashlib

st.set_page_config(page_title="finAIguard: Web3 Compliance/Fraud Engine", layout="centered")

# --- Metamask Connect (Streamlit-Components JS Injection) ---
st.markdown("""
<script>
if (typeof window.ethereum !== "undefined") {
    window.accountInterval = setInterval(async () => {
        const accounts = await window.ethereum.request({ method: 'eth_accounts' });
        const statusDiv = document.getElementById("walletStatus");
        if (accounts.length > 0 && statusDiv) {
            statusDiv.innerText = "🦊 Connected: " + accounts[0].substring(0,7) + "...";
        } else if (statusDiv) {
            statusDiv.innerText = "NOT Connected! Click below ⬇";
        }
    }, 1100);
    window.connectWallet = async function() {
        await ethereum.request({ method: 'eth_requestAccounts' });
    }
}
</script>
""", unsafe_allow_html=True)
st.markdown("""
<div style='margin-top:0.7em; font-size:1.13em; font-weight:500;'>
    <div id='walletStatus' style='color: #8323FF;'>Checking MetaMask status...</div>
    <button onclick='connectWallet()' style='background:#8323FF;border-radius:8px;color:#fff;padding:7.5px 1.2em;margin-top:0.7em;cursor:pointer;font-size:1.01em;'>Connect MetaMask Wallet</button>
</div>
""", unsafe_allow_html=True)

st.markdown("""
# <span style='color:#000'>finAIguard 🔮</span>
**Live Web3 Compliance & Fraud Detection (Crypto Only)**
""", unsafe_allow_html=True)

st.write("""
- Uses real-time prices from CoinMarketCap for any crypto.
- Checks compliance (for demo: price > $10k = flag).
- Blockchain-proof hash for each check.
- Fully Web3—connect your MetaMask to prove identity (coming soon: true POAP/NFT functions!).
""")

cmc_api_key = st.text_input("Your CoinMarketCap API Key", type="password")
crypto_symbols = st.text_input("Crypto symbols (comma-separated: e.g. BTC,ETH,MATIC):", "BTC,ETH")

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

def isnumber_finite(x):
    try:
        return np.isfinite(float(x))
    except Exception:
        return False

def fmt_price(x):
    try:
        return f"{float(x):,.2f}"
    except Exception:
        return "N/A"

if st.button("🔍 Check Latest Trades (Crypto Only, Live)"):
    cryptos = [s.strip().upper() for s in crypto_symbols.split(',') if s.strip()]
    trade_rows = []
    for csym in cryptos:
        if not cmc_api_key:
            st.error(f"CMC API Key required for {csym}!")
            st.stop()
        price = fetch_cmc_price(csym, cmc_api_key)
        if not isnumber_finite(price):
            continue
        trade_rows.append({
            'timestamp': datetime.utcnow(),
            'symbol': csym + '-USD',
            'price': price,
            'trade_type': 'Crypto',
            'action': 'LIVE',
        })
    df_trades = pd.DataFrame(trade_rows)
    if df_trades.empty:
        st.error("No valid prices found. Symbol typo? API problem? Try again.")
        st.stop()

    def check_compliance(row):
        breaches = []
        if isnumber_finite(row['price']) and float(row['price']) > 10000:
            breaches.append("Price > $10k: Flagged!")
        return breaches

    df_trades['compliance_breaches'] = df_trades.apply(check_compliance, axis=1)
    df_trades['blockchain_hash'] = df_trades.apply(
        lambda x: hashlib.sha256(str(x.to_dict()).encode()).hexdigest()[:20], axis=1)

    st.success(f"Checked {len(df_trades)} coins live! All results are below.")
    st.dataframe(df_trades[['timestamp','symbol','price','compliance_breaches','blockchain_hash']], use_container_width=True)

    st.markdown("### ⛓️ _How to mint a POAP/NFT proof on-chain_")
    st.code("""
# JS/Web3 Example (not directly in Streamlit but for your DApp/extension)
await contract.methods.mintNFT(wallet_address, blockchain_hash).send({from: wallet_address})
    """, language="python")
    st.write(
        "Once connected, you can use an NFT contract + your hash to mint a true compliance POAP NFT. "
        "Feature is coming soon to Streamlit via ethers.js/web3.js + Background server integration!"
    )
    st.info("Questions? Want real minting right here? Let us know at @finAIguard!")
else:
    st.info("Enter CMC API key & crypto symbol(s), connect MetaMask, then check compliance/fraud (live, no simulation).")
