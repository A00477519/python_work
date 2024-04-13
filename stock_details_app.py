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

# Function to fetch historical price data for a given cryptocurrency
def get_historical_price(crypto_id):
    # Fetch historical price data for the past 1 year (52 weeks)
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart?vs_currency=usd&days=365"
    response = requests.get(url)
    data = response.json()

    # Extracting prices from the response
    prices = data['prices']

    # Convert to DataFrame
    df = pd.DataFrame(prices, columns=['timestamp', 'price'])

    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    return df

# Function to plot the coin's price over the last year
def plot_price(df, crypto_name):
    plt.figure(figsize=(10, 6))
    plt.plot(df['timestamp'], df['price'], marker='o', linestyle='-')
    plt.title(f"{crypto_name} Price Over Last Year")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.grid(True)
    st.pyplot()

# Main function
def main():
    # Fetching the list of available cryptocurrencies
    url = "https://api.coingecko.com/api/v3/coins/list"
    response = requests.get(url)
    coins = response.json()

    # Displaying the app title and description
    st.title("Question 1 - Stock Details Analysis")
    st.write("This app allows us to analyze the price history of cryptocurrencies.")

    # User input for selecting a cryptocurrency
    crypto_name = st.text_input("Enter the name of the cryptocurrency:")

    # Finding the ID of the selected cryptocurrency
    crypto_id = None
    for coin in coins:
        if coin['name'].lower() == crypto_name.lower():
            crypto_id = coin['id']
            break

    if crypto_id:
        st.write(f"Fetching data for {crypto_name}...")

        # Fetch historical price data
        df = get_historical_price(crypto_id)

        # Plot the coin's price over the last year
        plot_price(df, crypto_name)

        # Calculate and display max and min prices
        max_price = df['price'].max()
        min_price = df['price'].min()
        st.write(f"Maximum price in the last year: ${max_price:.2f}")
        st.write(f"Minimum price in the last year: ${min_price:.2f}")

        # Find the day when it traded at the highest and lowest prices
        max_price_date = df.loc[df['price'].idxmax(), 'timestamp']
        min_price_date = df.loc[df['price'].idxmin(), 'timestamp']
        st.write(f"The day with the highest price: {max_price_date.strftime('%Y-%m-%d')}")
        st.write(f"The day with the lowest price: {min_price_date.strftime('%Y-%m-%d')}")

    else:
        st.write("Please enter a valid cryptocurrency name.")

# Run the app
if __name__ == "__main__":
    main()
    
    


