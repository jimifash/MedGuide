import os
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# --- Load environment variables ---
load_dotenv()

# --- Initialize Supabase Engine ---
DATABASE_URL = os.getenv("SUPABASE_URL")

if not DATABASE_URL:
    raise ValueError("❌ SUPABASE_URL not found in .env file!")

# Use SSL for Supabase PostgreSQL
engine = create_engine(DATABASE_URL, connect_args={"sslmode": "require"})


# --- CREATE TABLES IN SUPABASE ---
def init_supabase_db():
    """Creates tables in Supabase PostgreSQL if they don't exist."""
    create_queries = """
    CREATE TABLE IF NOT EXISTS bookings (
        id SERIAL PRIMARY KEY,
        Name TEXT,
        Email TEXT,
        Preferred_Date DATE,
        Preferred_Time TEXT,
        Problem TEXT,
        Start_date TEXT,
        Current_condition_after_start TEXT,
        Severity INTEGER,
        Occured_Before TEXT,
        Medication_taken TEXT,
        Fever TEXT,
        Pain TEXT,
        Cough_Cold_Breath_Shortness TEXT,
        Change_in_appetite_weight TEXT,
        Chronic_Conditions TEXT,
        Current_Medication TEXT,
        Allergies TEXT,
        Past_Hospitalization_Surgery TEXT,
        Smoke_or_Alcohol TEXT,
        Sleep_Hours INTEGER,
        Exercise_Frequency TEXT,
        Stress_Fatigue TEXT,
        Women_Status TEXT,
        Other_Notes TEXT,
        Submitted_On TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS predictions (
        id SERIAL PRIMARY KEY,
        Name TEXT,
        Age INTEGER,
        Gender TEXT,
        Fever REAL,
        Cough INTEGER,
        Headache INTEGER,
        Fatigue INTEGER,
        Nausea INTEGER,
        Muscle_Pain INTEGER,
        Shortness_of_Breath INTEGER,
        Loss_of_Taste INTEGER,
        Abdominal_Pain INTEGER,
        Appetite_Loss INTEGER,
        Frequent_Urination INTEGER,
        Thirst_Level INTEGER,
        Blurred_Vision INTEGER,
        Symptom_Duration_Days INTEGER,
        Severity INTEGER,
        Predicted_Disease TEXT,
        Predicted_On TIMESTAMP
    );
    """
    with engine.begin() as conn:
        conn.execute(text(create_queries))
    print("✅ Supabase tables initialized!")


# --- SAVE FORM DATA ---
def save_booking_to_db(data):
    """Save booking info to Supabase PostgreSQL."""
    data = {k.replace(" ", "_").replace("/", "_"): v for k, v in data.items()}

    if "Submitted_On" not in data:
        data["Submitted_On"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    columns = ", ".join(data.keys())
    placeholders = ", ".join([f":{col}" for col in data.keys()])
    query = text(f"INSERT INTO bookings ({columns}) VALUES ({placeholders})")

    with engine.begin() as conn:
        conn.execute(query, data)

    print("✅ Booking saved successfully!")


# --- SAVE PREDICTIONS ---
def save_predictions_to_db(pred_data):
    """Save prediction results to Supabase PostgreSQL database."""
    if "Predicted_On" not in pred_data:
        pred_data["Predicted_On"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    columns = ", ".join(pred_data.keys())
    placeholders = ", ".join([f":{col}" for col in pred_data.keys()])
    query = text(f"INSERT INTO predictions ({columns}) VALUES ({placeholders})")

    with engine.begin() as conn:
        conn.execute(query, pred_data)

    print("✅ Prediction saved successfully!")


# --- FETCH ALL BOOKINGS ---
def get_all_bookings():
    """Retrieve all bookings from Supabase."""
    query = "SELECT * FROM bookings ORDER BY id DESC"
    with engine.connect() as conn:
        df = pd.read_sql_query(query, conn)
    return df


# --- FETCH ALL PREDICTIONS ---
def get_all_predictions():
    """Retrieve all predictions from Supabase."""
    query = "SELECT * FROM predictions ORDER BY id DESC"
    with engine.connect() as conn:
        df = pd.read_sql_query(query, conn)
    return df


# --- DELETE A BOOKING ---
def delete_booking(record_id):
    """Deletes a booking record by ID."""
    query = text("DELETE FROM bookings WHERE id = :id")
    with engine.begin() as conn:
        conn.execute(query, {"id": record_id})
    print(f"🗑️ Booking with ID {record_id} deleted.")


# --- Run this manually once to ensure tables exist ---
if __name__ == "__main__":
    init_supabase_db()
