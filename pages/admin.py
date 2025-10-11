# admin_page.py
import streamlit as st
import pandas as pd
import sqlite3
from booking_pipeline import get_all_bookings

st.title("🔒 Admin Dashboard")

access_code = st.text_input("Enter access code:", type="password")

if access_code == "mysecret123":
    df = get_all_bookings()
    st.dataframe(df)

    st.download_button("Download booking CSV", df.to_csv(index=False), "bookings.csv")
else:
    st.warning("Enter valid access code to view data")
