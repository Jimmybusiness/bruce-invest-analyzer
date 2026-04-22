import streamlit as st
import yfinance as yf

st.set_page_config(page_title='Bruce Invest Analyzer', page_icon='📈')

def main():
    st.title('📈 Bruce Invest Analyzer')
    ticker = st.text_input('Rechercher une entreprise (ex: TTE.PA)', value='TTE.PA')
    if ticker:
        stock = yf.Ticker(ticker)
        st.write(stock.info.get('longName', ticker))
        st.metric('Prix', stock.info.get('currentPrice'))

if __name__ == '__main__': main()