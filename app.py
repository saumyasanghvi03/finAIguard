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
<span class='bigfont' style='color: #000000;'>finAIguard 🔮</span> — 
<span style='font-size:1.3em;'>Bridging Web3 🚀 & TradFi 🏦 with AI-powered Compliance & Fraud Detection</span><br>
<span style='color: #F9D923; font-size:1.08em;'>GenZ Ready. DeFi Native. Market Secure.</span>
</div>
""", unsafe_allow_html=True)
