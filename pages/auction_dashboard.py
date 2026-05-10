import streamlit as st
import pandas as pd
import time
import math

JSON_FILE = "bids_log.txt"

###########
# sidebar #
###########
try:
    full_df = pd.read_json(JSON_FILE, lines=True)
    unique_vals = full_df['auction_id'].unique()
    option = st.sidebar.selectbox('Select Auction Item', unique_vals)
except FileNotFoundError:
    st.sidebar.error("JSON file not found.")


filtered_df = full_df[full_df['auction_id'] == option]
st.line_chart(filtered_df, x='timestamp', y='amount')
