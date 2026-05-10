import streamlit as st
import pandas as pd
from confluent_kafka import Producer
import json, random, datetime, time
import time
import math

JSON_FILE = "bids_log.txt"
config={'bootstrap.servers': 'localhost:9092'}
producer = Producer(config)

st.sidebar.page_link("http://localhost:8080", label="Go to Kafka Dashboard")
st.write("The following items are currently up for auction:")
try:
    full_df = pd.read_json(JSON_FILE, lines=True)
    unique_vals = full_df['auction_id'].unique()
    for item in unique_vals:
        st.write(f"- {item}")
except FileNotFoundError:
    st.error("JSON file not found.")

@st.dialog("Place a Bid")
def bid_dialog():
    auction_item = st.selectbox('Select Auction Item', unique_vals)
    user_name = st.text_input("Your Name")
    bid_amount = st.number_input("Bid Amount ($)", min_value=0)
    if st.button("Submit Bid"):
        new_bid = {
            "auction_id": auction_item,
            "user_id": user_name,
            "amount": bid_amount,
            "timestamp": time.strftime('%H:%M:%S')
        }
        #send this bid to validation
        producer.produce('live-bids', value=json.dumps(new_bid))
        st.rerun()


if st.button("Place a Bid"):
    bid_dialog()

# Polling function to refresh data every 5 seconds
@st.fragment(run_every=5)
def auto_refresh_data():
    try:
        full_df = pd.read_json(JSON_FILE, lines=True)
        now = pd.Timestamp.now()
        highest_df = full_df.groupby('auction_id', as_index=True).agg({
            'amount': 'max',
            'user_id': 'last',
            'timestamp': 'last'
        })
        st.subheader("Current Highest Bids")
        st.dataframe(highest_df,
                     column_config={
                         "auction_id": st.column_config.TextColumn("Item"),
                         "amount": st.column_config.NumberColumn("Bid Amount ($)"),
                         "user_id": st.column_config.TextColumn("User"),
                     },
                     column_order=["auction_id", "amount", "user_id"])
        st.caption(f"Last updated: {time.strftime('%H:%M:%S')}")
        full_df['timestamp'] = full_df['timestamp'].apply(lambda x: (now - pd.to_datetime(x)).seconds / 60)
        notifications = full_df.sort_values('timestamp', ascending=True).head(5)
        st.subheader("Recent Actions")
        for _, row in notifications.iterrows():
            st.write(f"User {row['user_id']} bid ${row['amount']} on {row['auction_id']} {math.trunc(row['timestamp'])} minutes ago")
    except FileNotFoundError:
        st.error("JSON file not found.")

auto_refresh_data()
