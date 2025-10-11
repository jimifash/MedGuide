import sqlite3
from datetime import datetime
import pandas as pd

# --- DATABASE INITIALIZATION ---
def init_db(db_name="phc_bookings.db"):
    """
    Initializes the SQLite database and creates the bookings table if it doesn't exist.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
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
        Submitted_On DATE
    )
    """)
    conn.commit()
    conn.close()


# --- SAVE FORM DATA ---
def save_booking_to_db(data, db_name="phc_bookings.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Ensure columns match DB schema
    data = {k.replace(" ", "_").replace("/", "_"): v for k, v in data.items()}

    # Ensure Submitted_On exists
    if "Submitted_On" not in data:
        data["Submitted_On"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    columns = ", ".join(data.keys())
    placeholders = ", ".join(["?"] * len(data))
    values = list(data.values())

    query = f"INSERT INTO bookings ({columns}) VALUES ({placeholders})"
    values = tuple(str(v) for v in values)
    cursor.execute(query, values)

    conn.commit()
    conn.close()



# --- FETCH ALL BOOKINGS ---
def get_all_bookings(db_name="phc_bookings.db"):
    """
    Retrieves all booking records from the SQLite database as a pandas DataFrame.
    """
    conn = sqlite3.connect(db_name)
    df = pd.read_sql_query("SELECT * FROM bookings ORDER BY id DESC", conn)
    conn.close()
    return df


# --- DELETE RECORD (admin feature) ---
def delete_booking(record_id, db_name="phc_bookings.db"):
    """
    Deletes a booking record by ID.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM bookings WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()
