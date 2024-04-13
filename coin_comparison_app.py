#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 20:00:30 2024

@author: papantiamoah

Python assignment - question 2
"""

import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Function to fetch historical price data for a given cryptocurrency
def get_historical_price(crypto_id, days):
    # Fetch historical price data for the specified number of days
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart?vs_currency=usd&days={days}"
    response = requests.get(url)
    data = response.json()

    # Extracting prices from the response
    prices = data['prices']

    # Convert to DataFrame
    df = pd.DataFrame(prices, columns=['timestamp', 'price'])

    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    return df

# Function to plot the coin's price over the specified time frame
def plot_price(df1, df2, crypto_name1, crypto_name2):
    plt.figure(figsize=(10, 6))
    plt.plot(df1['timestamp'], df1['price'], label=crypto_name1, marker='o', linestyle='-')
    plt.plot(df2['timestamp'], df2['price'], label=crypto_name2, marker='o', linestyle='-')
    plt.title("Cryptocurrency Price Comparison")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.legend()
    plt.grid(True)
    st.pyplot()

# Main function
def main():
    # Fetching the list of available cryptocurrencies
    url = "https://api.coingecko.com/api/v3/coins/list"
    response = requests.get(url)
    coins = response.json()

    # Displaying the app title and description
    st.title("Coin Comparison")
    st.write("This app allows us to compare the price performance of two coins over different time frames.")

    if isinstance(coins, list) and all(isinstance(coin, dict) for coin in coins):
    # User input for selecting the first cryptocurrency
        crypto_name1 = st.text_input("Enter the name of the first cryptocurrency:")
        crypto_id1 = None
        if crypto_name1:
            for coin in coins:
                if 'name' in coin and coin['name'].lower() == crypto_name1.lower():
                    crypto_id1 = coin['id']
                    break

    # Further processing...
    else:
        st.write("Failed to fetch or parse cryptocurrency data.")

    # User input for selecting the second cryptocurrency
    crypto_name2 = st.text_input("Enter the name of the second cryptocurrency:")

    # Finding the ID of the selected cryptocurrency
    crypto_id2 = None
    for coin in coins:
        if coin['name'].lower() == crypto_name2.lower():
            crypto_id2 = coin['id']
            break

    # User input for selecting the time frame
    timeframe = st.selectbox("Select the time frame:", ["1 week", "1 month", "1 year", "5 years"])

    # Mapping time frame to number of days
    timeframe_mapping = {"1 week": 7, "1 month": 30, "1 year": 365, "5 years": 1825}
    days = timeframe_mapping[timeframe]

    if crypto_id1 and crypto_id2:
        st.write(f"Fetching data for {crypto_name1} and {crypto_name2}...")

        # Fetch historical price data for the first cryptocurrency
        df1 = get_historical_price(crypto_id1, days)

        # Fetch historical price data for the second cryptocurrency
        df2 = get_historical_price(crypto_id2, days)

        # Plot the price comparison
        plot_price(df1, df2, crypto_name1, crypto_name2)

    else:
        st.write("Please enter valid cryptocurrency names.")

# Run the app
if __name__ == "__main__":
    main()
