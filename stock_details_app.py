#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 19:49:24 2024

@author: papantiamoah

Python assignment - question 1
"""

import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# CoinGecko API URL for coins list
#COINS_LIST_URL = "https://api.coingecko.com/api/v3/coins/list"

# Fetch the list of available coins and their IDs
def fetch_coins():
    COINS_LIST_URL = "https://api.coingecko.com/api/v3/coins/list"
    try:
        response = requests.get(COINS_LIST_URL)
        response.raise_for_status()  # Will raise an exception for HTTP error codes
        coins = response.json()

        # Debugging: Check the type and sample data
        print(f"Type of coins variable: {type(coins)}")
        if isinstance(coins, list) and coins:
            print(f"Sample coin entry: {coins[0]}")
        else:
            print("Coins is not a list or is empty")
            return {}

        return {coin['name']: coin['id'] for coin in coins if 'name' in coin and 'id' in coin}
    except requests.HTTPError as e:
        print(f"HTTP error occurred: {e}")  # HTTP error
        return {}
    except Exception as e:
        print(f"An error occurred: {e}")  # Other errors
        return {}


# Streamlit UI
st.title('Cryptocurrency Price Tracker')
selected_coin = st.selectbox('Select a Cryptocurrency', list(coins.keys()))

# Fetch historical data for the selected coin
def fetch_coin_data(coin_id, days=365):
    HISTORICAL_DATA_URL = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency=usd&days={days}"
    response = requests.get(HISTORICAL_DATA_URL)
    data = response.json()
    prices = data['prices']
    df = pd.DataFrame(prices, columns=['Timestamp', 'Price'])
    df['Date'] = pd.to_datetime(df['Timestamp'], unit='ms')
    df.set_index('Date', inplace=True)
    return df.drop('Timestamp', axis=1)

if selected_coin:
    coin_id = coins[selected_coin]
    df = fetch_coin_data(coin_id)
    st.line_chart(df)

    # Display max and min prices
    max_price = df['Price'].max()
    min_price = df['Price'].min()
    max_date = df['Price'].idxmax().strftime('%Y-%m-%d')
    min_date = df['Price'].idxmin().strftime('%Y-%m-%d')
    
    st.write(f"Maximum Price: ${max_price} on {max_date}")
    st.write(f"Minimum Price: ${min_price} on {min_date}")
