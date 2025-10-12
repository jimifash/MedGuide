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
        name TEXT,
        email TEXT,
        gender TEXT,
        phone_number VARCHAR(25),
        preferred_date DATE,
        preferred_time TEXT,
        problem TEXT,
        start_date TEXT,
        current_condition_after_start TEXT,
        severity INTEGER,
        occured_before TEXT,
        medication_taken TEXT,
        fever TEXT,
        pain TEXT,
        cough_cold_breath_shortness TEXT,
        change_in_appetite_weight TEXT,
        chronic_conditions TEXT,
        current_medication TEXT,
        allergies TEXT,
        past_hospitalization_surgery TEXT,
        smoke_or_alcohol TEXT,
        sleep_hours INTEGER,
        exercise_frequency TEXT,
        stress_fatigue TEXT,
        women_status TEXT,
        other_notes TEXT,
        submitted_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS predictions (
        id SERIAL PRIMARY KEY,
        name TEXT,
        age INTEGER,
        gender TEXT,
        fever REAL,
        cough INTEGER,
        headache INTEGER,
        fatigue INTEGER,
        nausea INTEGER,
        muscle_pain INTEGER,
        shortness_of_breath INTEGER,
        loss_of_taste INTEGER,
        abdominal_pain INTEGER,
        appetite_loss INTEGER,
        frequent_urination INTEGER,
        thirst_level INTEGER,
        blurred_vision INTEGER,
        symptom_duration_days INTEGER,
        severity INTEGER,
        predicted_disease TEXT,
        predicted_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    with engine.begin() as conn:
        conn.execute(text(create_queries))
    print("✅ Supabase tables initialized!")


# --- SAVE FORM DATA ---
def save_booking_to_db(data):
    """Save booking info to Supabase PostgreSQL."""
    
    # Flatten any single-item lists (e.g., from Streamlit widgets)
    for key, value in data.items():
        if isinstance(value, list):
            data[key] = ", ".join(map(str, value))  # Join multiple selections into a string

    # Standardize column names
    data = {k.replace(" ", "_").replace("/", "_"): v for k, v in data.items()}

    # Add submission timestamp if missing
    data.pop("Submitted_On", None)
    data.pop("submitted_on", None)

    # Add clean lowercase version
    data["submitted_on"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Build SQL query
    columns = ", ".join(data.keys())
    placeholders = ", ".join([f":{col}" for col in data.keys()])
    query = text(f"INSERT INTO bookings ({columns}) VALUES ({placeholders})")

    with engine.begin() as conn:
        conn.execute(query, data)

    print("✅ Booking saved successfully!")


# --- SAVE PREDICTIONS ---
def save_predictions_to_db(pred_data):
    """Save prediction results to Supabase PostgreSQL database."""
    
    # Add prediction timestamp if missing
    if "predicted_on" not in pred_data:
        pred_data["predicted_on"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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
    """Fetch all predictions from Supabase PostgreSQL."""
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
