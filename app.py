import streamlit as st
import streamlit.components.v1 as components
import yfinance as yf
import plotly.graph_objects as go
import requests

ICON_URL = "https://static.prod-images.emergentagent.com/jobs/0ea31682-e703-443e-9b36-d0c5d54ebbbd/images/9cc3508b7c1dc15bdbff80f59fee054105a6b829ce1f04a00bd316d2fe2ac431.jpeg"

st.set_page_config(page_title="Bruce Invest Analyzer", page_icon=ICON_URL, layout="centered")

def inject_ios_icon():
    components.html(f"""
    <script>
        var link = window.parent.document.createElement('link');
        link.rel = 'apple-touch-icon';
        link.href = '{ICON_URL}';
        window.parent.document.head.appendChild(link);
    </script>
    """, height=0)

def inject_css():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
html, body, [data-testid="stAppViewContainer"] { font-family: 'Inter', sans-serif !important; background-color: #0F0F12 !important; color: #FFFFFF !important; }
.block-container { max-width: 480px !important; padding: 1rem !important; }
#MainMenu, footer, header { display: none !important; }
.app-header { background: linear-gradient(135deg, #4169E1 0%, #C0C0C0 100%); border-radius: 20px; padding: 20px; margin-bottom: 20px; text-align: center; border: 1px solid #2C2C2E; }
.app-header h1 { font-size: 22px !important; margin: 0 !important; color: #FFFFFF !important; text-shadow: 0 1px 3px rgba(0,0,0,0.3); }
.card { background: #1C1C1E; border-radius: 16px; padding: 14px; margin-bottom: 10px; border: 1px solid #2C2C2E; text-align: center; }
.price { font-size: 24px; font-weight: 800; color: #FFFFFF; }
.label { font-size: 10px; color: #C0C0C0; text-transform: uppercase; font-weight: 700; margin-bottom: 4px; }
.score-box { background: linear-gradient(135deg, #4169E1 0%, #6A5ACD 100%); border-radius: 12px; padding: 12px; text-align: center; margin: 10px 0; }
.score-val { font-size: 26px; font-weight: 900; color: white; }
.bruce-avis { background: #1C1C1E; border-radius: 16px; padding: 15px; border-left: 4px solid #4169E1; margin-top: 15px; }
.bullet { display: flex; align-items: flex-start; gap: 10px; margin-bottom: 8px; font-size: 13px; line-height: 1.4; }
div.stButton > button { width: 100% !important; background-color: #2C2C2E !important; color: #FFFFFF !important; border: 1px solid #3A3A3C !important; border-radius: 12px !important; padding: 10px !important; font-weight: 600 !important; }
div.stButton > button:hover { background-color: #4169E1 !important; }
</style>
""", unsafe_allow_html=True)

def get_ticker_suggestions(query):
    if len(query) < 2: return []
    url = f"https://query2.finance.yahoo.com/v1/finance/search?q={query}&quotesCount=5"
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        resp = requests.get(url, headers=headers)
        return resp.json().get('quotes', [])
    except: return []

def main():
    inject_ios_icon()
    inject_css()
    st.markdown('<div class="app-header"><h1>📈 Bruce Invest Analyzer</h1></div>', unsafe_allow_html=True)
    if 'selected_ticker' not in st.session_state: st.session_state.selected_ticker = "TTE.PA"
    if 'search_key' not in st.session_state: st.session_state.search_key = 0
    search_query = st.text_input("Rechercher une entreprise", key=f"search_input_{st.session_state.search_key}", placeholder="Tapez le nom ici...")
    if search_query:
        suggestions = get_ticker_suggestions(search_query)
        if suggestions:
            for s in suggestions:
                symbol = s.get('symbol')
                if st.button(f"{symbol} \u2014 {s.get('shortname', symbol)}", key=f"btn_{symbol}"):
                    st.session_state.selected_ticker = symbol
                    st.session_state.search_key += 1
                    st.rerun()
    ticker = st.session_state.selected_ticker
    try:
        with st.spinner("Analyse..."):
            stock = yf.Ticker(ticker)
            info = stock.info
            hist = stock.history(period="1y")
        price = info.get('currentPrice') or info.get('regularMarketPreviousClose') or 0
        currency = info.get('currency', '\u20ac')
        div_rate = info.get('dividendRate', 0) or 0
        raw_yield = info.get('dividendYield', 0) or 0
        yield_pct = raw_yield * 100 if raw_yield < 1 else raw_yield
        pe = info.get('trailingPE', 0) or 0
        
        st.markdown(f"### {info.get('longName', ticker)}")
        
        # Row 1: Price and Dividend Amount
        c1, c2 = st.columns(2)
        with c1: st.markdown(f'<div class="card"><div class="label">Prix Actuel</div><div class="price">{price:.2f}<small>{currency}</small></div></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="card"><div class="label">Dividende / Action</div><div class="price" style="color:#5AC8FA">{div_rate:.2f}<small>{currency}</small></div></div>', unsafe_allow_html=True)
        
        # Row 2: Yield and P/E
        c3, c4 = st.columns(2)
        with c3: st.markdown(f'<div class="card"><div class="label">Rendement</div><div class="price" style="color:#34C759">{yield_pct:.1f}%</div></div>', unsafe_allow_html=True)
        with c4:
            pe_color = "#34C759" if 0 < pe < 15 else "#FF9500" if pe < 25 else "#FF3B30"
            st.markdown(f'<div class="card"><div class="label">Ratio P/E</div><div class="price" style="color:{pe_color}">{pe:.1f}</div></div>', unsafe_allow_html=True)
        
        score = 5
        if yield_pct > 5: score += 2
        if 0 < pe < 15: score += 2
        st.markdown(f'<div class="score-box"><div class="label" style="color:white">Score Bruce</div><div class="score-val">{min(10, score)}/10</div></div>', unsafe_allow_html=True)
        
        fig = go.Figure(data=[go.Scatter(x=hist.index, y=hist['Close'], line=dict(color='#4169E1', width=3))])
        fig.update_layout(height=180, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis=dict(showgrid=False), yaxis=dict(showgrid=False), font=dict(color="white"))
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

        st.markdown('<div class="bruce-avis"><b>\ud83e\udde0 AVIS DE BRUCE</b><br><br>' +
            f'<div class="bullet">\u2705 <b>Valorisation</b> : {"Attrayante" if pe < 15 else "Correcte" if pe < 25 else "\u00c9lev\u00e9e"}.</div>' +
            f'<div class="bullet">\u2705 <b>Dividende</b> : {"Excellent" if yield_pct > 5 else "Correct" if yield_pct > 0 else "Nul"}.</div>' +
            f'<div class="bullet">\ud83d\ude80 <b>Verdict</b> : {"Action id\u00e9ale pour le rendement !" if score >= 7 else "\u00c0 surveiller patiemment."}</div></div>', unsafe_allow_html=True)
    except: st.error("Erreur d'analyse.")

if __name__ == "__main__": main()
