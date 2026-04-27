import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import datetime
st.set_page_config(page_title = "Portfolio analysis", layout="wide")

st.title ("portfolio app")

st.sidebar.header("User input")

st.sidebar.header("Portfolio Input")

stock_tickers = []
stock_weights = []

for i in range(1, 6):
    ticker = st.sidebar.text_input(f"Stock {i} Ticker", key=f"ticker_{i}")
    weight = st.sidebar.number_input(f"Stock {i} Weight (%) (0-100)", min_value=0.0, max_value=100.0, value=0.0, step=0.1, key=f"weight_{i}")
    stock_tickers.append(ticker)
    stock_weights.append(weight)

end_date = datetime.date.today()
start_date = end_date - datetime.timedelta(days=365)

start = st.sidebar.date_input('Start Date', start_date)
end = st.sidebar.date_input('End Date', end_date)

if st.sidebar.button('Get Data'):
    st.subheader('Fetching Data...')

    stock_data = {}
    valid_tickers = [ticker for ticker in stock_tickers if ticker]

    if not valid_tickers:
        st.error("Please enter at least one stock ticker.")
    else:
        for ticker in valid_tickers:
            try:
                df = yf.download(ticker, start=start, end=end)
                if df.empty:
                    st.error(f"No Data Found for {ticker}. Please check the ticker symbol or date range.")
                else:
                    stock_data[ticker] = df
                    st.success(f"Data Successfully extracted for {ticker}")
            except Exception as e:
                st.error(f"Error fetching data for {ticker}: {e}")
        if stock_data:
            first_ticker = list(stock_data.keys())[0]
            st.write(f"Preview of data for {first_ticker}:")
            st.dataframe(stock_data[first_ticker].head())
