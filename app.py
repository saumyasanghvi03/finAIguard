import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import hashlib

st.set_page_config(page_title="finAIguard: Web3 Crypto Compliance", layout="centered")
st.markdown("""
# <span style='color:#000'>finAIguard 🔮</span>
**Web3 Crypto Compliance & Fraud Detection**
""", unsafe_allow_html=True)

st.write("For real wallet-linked compliance proof, use a true DApp with WalletConnect modal below, or paste your address for demo only.")

wallet_address = st.text_input("Paste your Wallet Address (for demo, not real connect):")
cmc_api_key = st.text_input("Your CoinMarketCap API Key", type="password")
crypto_symbols = st.text_input("Crypto symbols (comma-separated: e.g. BTC,ETH,MATIC)", "BTC,ETH")

# WalletConnect link display (user should open it in a dApp for QR scan)
st.markdown(
    """
    [![Connect with WalletConnect](https://walletconnect.com/_next/static/media/logo_mark.014750fd.svg)](https://walletconnect.com/)
    <br>
    <b>Need real wallet <i>connect</i>? Launch a dApp or website built with WalletConnect's JS SDK.</b>
    <br>
    <i>This Streamlit demo is backend only and cannot do true wallet connect/signing due to browser security.</i>
    """,
    unsafe_allow_html=True
)

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
        return None

if st.button("🔍 Check Now (Crypto, Live)"):
    cryptos = [s.strip().upper() for s in crypto_symbols.split(',') if s.strip()]
    rows = []
    for csym in cryptos:
        if not cmc_api_key:
            st.error("CMC API key required!")
            st.stop()
        price = fetch_cmc_price(csym, cmc_api_key)
        if not price:
            continue
        rows.append({
            'timestamp': datetime.utcnow(),
            'symbol': csym + '-USD',
            'price': price,
            'wallet': wallet_address or "(not provided)",
            'compliance_breach': "YES" if price > 10000 else "",
            'proof_hash': hashlib.sha256(f"{csym}{price}{wallet_address}".encode()).hexdigest()[:20]
        })
    df = pd.DataFrame(rows)
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.error("No results (API/symbol error)!")

else:
    st.info("Enter wallet (for demo), CMC API key, and check for real-time compliance.")

st.markdown("""
---
#### How do I make my own **true** on-chain POAP/NFT compliance DApp?
- Use WalletConnect or MetaMask in a React/Vite web app.
- On user action, JS signs a message or mints an NFT with a backend- or frontend-generated hash.
- [WalletConnect JS/React Example](https://github.com/WalletConnect/walletconnect-modal-react-example)
- [MetaMask Docs](https://docs.metamask.io/wallet/how-to/)
""")
