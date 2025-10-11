import streamlit as st
import pandas as pd
from datetime import datetime
from prediction_pipeline import process_prediction  # your custom ML or saving pipeline
from train import accuracy


def page():
    st.set_page_config(page_title="Disease Prediction", layout="centered")

    st.title("🧬 Disease Prediction Assistant")
    st.write("Enter patient details and symptoms below:")
    st.write(f'model has{accuracy}% accuracy')

    # --- Patient Basic Info ---
    st.header("👤 Patient Information")
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age", min_value=0, max_value=120, value=30, step=1)
    with col2:
        gender = st.selectbox("Gender", ["Male", "Female"])


    # --- Symptoms Section ---
    st.header("🩺 Symptoms and Observations")

    col1, col2, col3 = st.columns(3)
    with col1:
        fever = st.number_input("Fever (°C)", min_value=35.0, max_value=42.0, step=0.1)
        cough = st.selectbox("Cough", [0, 1], help="0 = No, 1 = Yes")
        headache = st.selectbox("Headache",[0, 1], help="0 = No, 1 = Yes")
        fatigue = st.slider("Fatigue (1-5)", 0, 5, 0)
        nausea = st.slider("Nausea (0-5)", 0, 5, 0)

    with col2:
        muscle_pain = st.slider("Muscle Pain (0-5)", 0, 5, 0)
        shortness_of_breath = st.slider("Shortness of Breath(0-5)", 0, 5, 0)
        loss_of_taste = st.selectbox("Loss of Taste", [0, 1])
        abdominal_pain = st.slider("Abdominal Pain (0-5)", 0, 5, 0)
        appetite_loss = st.slider("Appetite Loss (0-5)", 0, 5, 0)

    with col3:
        frequent_urination = st.slider("Frequent Urination(0-5)", 0, 5, 0)
        thirst_level = st.slider("Thirst Level (0-5)", 0, 5, 0)
        blurred_vision = st.selectbox("Blurred Vision", [0, 1])
        symptom_duration = st.number_input("Symptom Duration (days)", min_value=0, max_value=90, value=0)
        severity = st.slider("Overall Severity (1-5)", 1, 5, 1)

    # --- Submit Button ---
    if st.button("🔍 Predict Disease / Save Record"):
        data = {
            "Age": [age],
            "Gender": [gender],
            "Fever": [fever],
            "Cough": [cough],
            "Headache": [headache],
            "Fatigue": [fatigue],
            "Nausea": [nausea],
            "Muscle_Pain": [muscle_pain],
            "Shortness_of_Breath": [shortness_of_breath],
            "Loss_of_Taste": [loss_of_taste],
            "Abdominal_Pain": [abdominal_pain],
            "Appetite_Loss": [appetite_loss],
            "Frequent_Urination": [frequent_urination],
            "Thirst_Level": [thirst_level],
            "Blurred_Vision": [blurred_vision],
            "Symptom_Duration_Days": [symptom_duration],
            "Severity(1-5)": [severity],
        }

        df = pd.DataFrame(data)
        st.write("### 🧾 Data Preview")
        st.dataframe(df)

        # Send to ML or database pipeline
        try:
            result = process_prediction(df)
            st.success(f"✅ Pipeline executed successfully! Result: {result}")
        except Exception as e:
            st.error(f"❌ Error in pipeline: {e}")
