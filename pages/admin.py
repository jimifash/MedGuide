import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from store_pipeline import get_all_bookings, get_all_predictions

st.set_page_config(page_title="Admin Dashboard", layout="wide")

st.title("🔒 Admin Dashboard")

# --- ACCESS CONTROL ---
access_code = st.text_input("Enter access code:", type="password")

if access_code != "ADMIN999":
    st.warning("Enter valid access code to view data")
    st.stop()

# --- LOAD DATA ---
bookings = get_all_bookings()
predictions = get_all_predictions()

# --- TABS FOR NAVIGATION ---
tab1, tab2, tab3 = st.tabs(["📘 Bookings Data", "🧠 Predictions Data", "📈 Insights Dashboard"])

# ==========================
# TAB 1: BOOKINGS DATA
# ==========================
with tab1:
    st.subheader("Bookings Data Overview")
    st.dataframe(bookings, use_container_width=True)

    st.download_button("📥 Download Bookings CSV", bookings.to_csv(index=False), "bookings.csv")

# ==========================
# TAB 2: PREDICTIONS DATA
# ==========================
with tab2:
    st.subheader("Predictions Data Overview")
    st.dataframe(predictions, use_container_width=True)

    st.download_button("📥 Download Predictions CSV", predictions.to_csv(index=False), "predictions.csv")

# ==========================
# TAB 3: INSIGHTS DASHBOARD
# ==========================
with tab3:
    st.subheader("📊 Interactive Data Insights")

    if predictions.empty:
        st.warning("No prediction data available.")
    else:
        # --- FILTERS ---
        with st.expander("🔍 Filters"):
            disease_filter = st.multiselect(
                "Select Diseases", options=predictions["Predicted_Disease"].unique(), default=None
            )

        df_filtered = predictions.copy()
        if disease_filter:
            df_filtered = df_filtered[df_filtered["Predicted_Disease"].isin(disease_filter)]

        # --- VISUALS ---
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Disease Frequency**")
            disease_count = df_filtered["Predicted_Disease"].value_counts().reset_index()
            disease_count.columns = ["Predicted_Disease", "Count"]
            fig = px.bar(
                disease_count, x="Predicted_Disease", y="Count",
                color="Predicted_Disease", title="Disease Distribution",
                text_auto=True
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("**Prediction Confidence / Probabilities (if available)**")
            numeric_cols = df_filtered.select_dtypes("number").columns
            if len(numeric_cols) > 0:
                fig2 = px.box(df_filtered, y=numeric_cols[0], color="Predicted_Disease",
                              title=f"Distribution of {numeric_cols[0]}")
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info("No numeric columns found for confidence visualization.")

        # --- TREND OVER TIME ---
        if "timestamp" in df_filtered.columns:
            df_filtered["timestamp"] = pd.to_datetime(df_filtered["timestamp"], errors='coerce')
            fig3 = px.line(df_filtered, x="timestamp", y=df_filtered.columns[0],
                           color="Disease", title="Prediction Trends Over Time")
            st.plotly_chart(fig3, use_container_width=True)

        st.markdown("---")
        st.markdown("### Summary Statistics")
        st.write(df_filtered.describe())
