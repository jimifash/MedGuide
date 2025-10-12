import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from store_pipeline import get_all_bookings, get_all_predictions
import datetime

st.set_page_config(page_title="Admin Dashboard", layout="wide")

st.title("🔒 Admin Dashboard")
st.write("Use: ADMIN999 as the password for this DEMO")

# --- ACCESS CONTROL ---
access_code = st.text_input("Enter access code:", type="password")

if access_code != "ADMIN999":
    st.warning("Enter valid access code to view data")
    st.stop()

# --- LOAD DATA ---
bookings = get_all_bookings()
predictions = get_all_predictions()

predictions.rename(columns={"predicted_disease": "Predicted_Disease"}, inplace=True)

# st.write("Predictions columns:", predictions.columns.tolist())
# st.write("Predictions rows:", predictions.shape[0])


# --- TABS FOR NAVIGATION ---
tab1, tab2, tab3, tab4 = st.tabs(["📘 Bookings Data", "🧠 Predictions Data", "📈 Insights Dashboard - Predictions", "📈 Insights Dashboard - Booking"])

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

# 🗓️ Booking Insights & Patient Trends
with tab4:
    st.subheader("🗓️ Booking Insights & Patient Trends")

    if bookings.empty:
        st.warning("No booking data available.")
    else:
        df_book = bookings.copy()
        df_book["submitted_on"] = pd.to_datetime(df_book["submitted_on"], errors="coerce")

        # --- FILTERS ---
        colf1, colf2, colf3 = st.columns(3)


        # 📅 DATE FILTER
  # --- FILTERS ---


# 📅 DATE FILTER
        with colf1:
            valid_dates = df_book["submitted_on"].dropna()
            if not valid_dates.empty:
                min_date, max_date = valid_dates.min().date(), valid_dates.max().date()
            else:
                today = pd.Timestamp.today().date()
                min_date = max_date = today

            default_value = (min_date, max_date) if min_date != max_date else min_date

            selected_dates = st.date_input(
                "Select Date Range",
                value=default_value,
                min_value=min_date,
                max_value=max_date
            )

            if isinstance(selected_dates, tuple):
                start_date, end_date = selected_dates
            else:
                start_date = end_date = selected_dates

            df_book = df_book[
                (df_book["submitted_on"].dt.date >= start_date)
                & (df_book["submitted_on"].dt.date <= end_date)
            ]

        # 👩 GENDER FILTER
        with colf2:
            gender_options = ["All"]
            if "gender" in df_book.columns:
                unique_genders = sorted([g for g in df_book["gender"].dropna().unique().tolist() if g])
                gender_options += unique_genders
            selected_gender = st.selectbox("Filter by Gender", gender_options)

            if selected_gender != "All":
                df_book = df_book[df_book["gender"] == selected_gender]

        # 💨 ALLERGY / LIFESTYLE FILTER
        with colf3:
            filter_type = st.radio("Filter By", ["Allergies", "Smoking/Alcohol"], horizontal=True)

            if filter_type == "Allergies" and "allergies" in df_book.columns:
                allergy_options = ["All"] + sorted(
                    set(
                        allergy.strip()
                        for sublist in df_book["allergies"]
                        .dropna()
                        .astype(str)
                        .str.replace("and", ",", regex=False)
                        .str.split(",")
                        for allergy in sublist
                    )
                )
                selected_allergy = st.selectbox("Select Allergy", allergy_options)
                if selected_allergy != "All":
                    df_book = df_book[df_book["allergies"].str.contains(selected_allergy, case=False, na=False)]

            elif filter_type == "Smoking/Alcohol" and "smoke_or_alcohol" in df_book.columns:
                habit_options = ["All"] + sorted(
                    set(
                        habit.strip()
                        for sublist in df_book["smoke_or_alcohol"]
                        .dropna()
                        .astype(str)
                        .str.replace("and", ",", regex=False)
                        .str.split(",")
                        for habit in sublist
                    )
                )
                selected_habit = st.selectbox("Select Habit", habit_options)
                if selected_habit != "All":
                    df_book = df_book[df_book["smoke_or_alcohol"].str.contains(selected_habit, case=False, na=False)]

        st.markdown("---")

        # --- GENDER DISTRIBUTION VISUALIZATION ---
        st.markdown("### 🚻 Gender Distribution Among Bookings")
        if "gender" in df_book.columns:
            gender_count = (
                df_book["gender"]
                .value_counts()
                .reset_index()
                .rename(columns={"index": "Gender", "gender": "Count"})
            )

            fig_gender = px.pie(
                gender_count,
                names="Gender",
                values="Count",
                title="Gender Distribution of Patients",
                color_discrete_sequence=px.colors.qualitative.Pastel,
                hole=0.3
            )
            st.plotly_chart(fig_gender, use_container_width=True)
        else:
            st.info("No 'gender' column found in booking records.")



        # --- APPLY FILTERS ---
        df_book = df_book[
            (df_book["submitted_on"].dt.date >= start_date)
            & (df_book["submitted_on"].dt.date <= end_date)
        ]
        if selected_gender != "All":
            df_book = df_book[df_book["gender"] == selected_gender]

        st.markdown("---")

        # ✅ VISUALS STILL SHOW EVEN IF DATA IS EMPTY
        if df_book.empty:
            st.info("No records match your selected filters.")
        else:
            # === FIRST ROW ===
            col1, col2 = st.columns(2)

            with col1:
                # 📅 Daily Bookings Trend
                bookings_per_day = (
                    df_book.groupby(df_book["submitted_on"].dt.date)
                    .size()
                    .reset_index(name="Count")
                    .sort_values("submitted_on")
                )
                bookings_per_day["Rolling_Avg"] = (
                    bookings_per_day["Count"].rolling(window=7, min_periods=1).mean()
                )
                fig = px.line(
                    bookings_per_day,
                    x="submitted_on",
                    y="Count",
                    title="Daily Bookings Trend",
                    markers=True,
                )
                fig.add_scatter(
                    x=bookings_per_day["submitted_on"],
                    y=bookings_per_day["Rolling_Avg"],
                    mode="lines",
                    name="7-Day Trend",
                    line=dict(width=3, dash="solid", color="orange"),
                )
                fig.update_layout(
                    xaxis=dict(title="Day", tickformat="%d %b", dtick="D1"),
                    yaxis_title="Bookings",
                    template="plotly_white",
                )
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                # 🧠 Health Problems
                if "problem" in df_book.columns:
                    problem_split = (
                        df_book["problem"]
                        .dropna()
                        .astype(str)
                        .str.replace("and", ",", regex=False)
                        .str.replace(r"[\[\]']", "", regex=True)
                        .str.split(",")
                        .explode()
                        .str.strip()
                        .value_counts()
                        .head(10)
                        .reset_index()
                    )
                    problem_split.columns = ["Health_Issue", "Count"]
                    fig2 = px.bar(
                        problem_split,
                        x="Health_Issue",
                        y="Count",
                        title="Top 10 Reported Health Issues",
                        text_auto=True,
                    )
                    st.plotly_chart(fig2, use_container_width=True)

            # === SECOND ROW ===
            col3, col4 = st.columns(2)

            with col3:
                # 🤧 Common Allergies
                if "allergies" in df_book.columns:
                    allergy_split = (
                        df_book["allergies"]
                        .dropna()
                        .astype(str)
                        .str.replace("and", ",", regex=False)
                        .str.split(",")
                        .explode()
                        .str.strip()
                        .value_counts()
                        .head(10)
                        .reset_index()
                    )
                    allergy_split.columns = ["Allergy", "Count"]
                    fig3 = px.bar(
                        allergy_split,
                        x="Allergy",
                        y="Count",
                        title="Most Common Allergies",
                        text_auto=True,
                        color="Allergy",
                    )
                    st.plotly_chart(fig3, use_container_width=True)

            with col4:
                # 🚬 Lifestyle Habits
                if "smoke_or_alcohol" in df_book.columns:
                    lifestyle_split = (
                        df_book["smoke_or_alcohol"]
                        .dropna()
                        .astype(str)
                        .str.replace("and", ",", regex=False)
                        .str.split(",")
                        .explode()
                        .str.strip()
                        .value_counts()
                        .reset_index()
                    )
                    lifestyle_split.columns = ["Habit", "Count"]
                    fig4 = px.bar(
                        lifestyle_split,
                        x="Habit",
                        y="Count",
                        title="Smoking or Alcohol Usage",
                        text_auto=True,
                        color="Habit",
                    )
                    st.plotly_chart(fig4, use_container_width=True)

        # --- WOMEN STATUS ---
        st.markdown("---")
        st.markdown("### 🤰 Women Status Distribution")
        if "women_status" in df_book.columns:
            women_status_count = (
                df_book["women_status"]
                .value_counts()
                .reset_index()
                .rename(columns={"index": "Status", "women_status": "Count"})
            )
            women_status_count.columns = ["Status", "Count"]

            fig5 = px.pie(
                women_status_count,
                names="Status",
                values="Count",
                title="Distribution of Women Status (e.g., Pregnant, Not Pregnant)",
                hole=0.4
            )
            st.plotly_chart(fig5, use_container_width=True)
        else:
            st.info("No 'Women_Status' column found in booking records.")

        # --- SUMMARY ---
        st.markdown("---")
        st.markdown("### 📈 Summary Stats")
        st.write(df_book.describe(include='all'))
