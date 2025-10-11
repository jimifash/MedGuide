import streamlit as st
from datetime import datetime
from translate_input import trans_text
from language_codes import LANGUAGES
from email_s import send_email
import pandas as pd
from booking_pipeline import init_db, save_booking_to_db

# Initialize DB once
init_db()

# --- PAGE CONFIG ---
st.set_page_config(page_title="MedGuide", layout="wide")

# --- SIDEBAR LANGUAGE SELECTOR ---
st.sidebar.title("🌍 Language Settings")
language = st.sidebar.selectbox(
    "Choose your preferred language:",
    LANGUAGES.keys(),
    index=0
)

# --- TRANSLATION HELPER ---
def T(text):
    """Translate text to user's chosen language"""
    if language == "en":
        return text
    try:
        return trans_text(text, language)
    except Exception:
        return text  # fallback if translation fails


# --- CUSTOM STYLES ---
st.markdown("""
    <style>
        body {
            background: linear-gradient(180deg, #007bff 0%, #b3d9ff 100%);
            color: #003366;
            font-family: 'Helvetica Neue', sans-serif;
        }
        .main { background: transparent; }

        h1, h2, h3 {
            color: #002b80;
            font-weight: 700;
        }

        .section {
            border-radius: 20px;
            padding: 40px 30px;
            margin: 30px 0px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }
        .section:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 25px rgba(0,0,0,0.15);
        }

        .stButton>button {
            background-color: #0066cc;
            color: white;
            border-radius: 10px;
            border: none;
            font-size: 16px;
            font-weight: 600;
            padding: 0.6em 1.5em;
        }
        .stButton>button:hover {
            background-color: #004d99;
            color: #ffffff;
        }

        .hero {
            background: linear-gradient(90deg, #0066cc 0%, #003366 100%);
            text-align: center;
            padding: 4rem 1rem 8rem 1rem;
            color: white;
            border-radius: 0 0 40px 40px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.15);
        }

        .news-card {
            background-color: #f8faff;
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 15px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }

        footer {
            text-align: center;
            color: #003366;
            margin-top: 50px;
            font-size: 0.9rem;
        }
    </style>
""", unsafe_allow_html=True)

# --- HERO SECTION ---
st.markdown(f"""
<div class="hero">
    <h1>{T("Health Assist")}</h1>
    <p>{T("Your Smart Companion for Quick First Aid, Health Tips, and Bookings")}</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1,1,1])
with col2:
    st.markdown("""
        <style>
            .black-btn {
                background-color: black;
                color: white;
                padding: 14px 36px;
                border-radius: 10px;
                border: none;
                font-size: 17px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.1s ease;
            }
            .black-btn:hover {
                background-color: #222;
                transform: scale(1.05);
            }
        </style>
    """, unsafe_allow_html=True)

    if st.button("💬 Try Quick Health AI"):
        st.switch_page("pages/main.py")


# --- BOOKING SECTION ---
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.header(f"📅 {T('Book a Health Consultation')}")

st.title(T("Doctor Appointment Booking Form"))

with st.form("booking_form"):
    st.subheader(T("Patient Information"))
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input(T("Full Name"))
        email = st.text_input(T("Email Address"))
    with col2:
        date = st.date_input(T("Preferred Date"), min_value=datetime.now().date())
        time = st.time_input(T("Preferred Time"))

    st.markdown("---")
    st.subheader(T("Health Information"))

    q1 = st.text_input(T("1. What health problem or symptom are you currently experiencing?"))
    q2 = st.text_input(T("2. When did the problem start?"))
    q3 = st.selectbox(T("3. Has the condition been getting better, worse, or staying the same?"),
                      [T("Better"), T("Worse"), T("Same")])
    q4 = st.slider(T("4. How severe is the symptom on a scale of 1 to 10?"), 1, 10, 5)
    q5 = st.radio(T("5. Have you had this problem before?"), [T("Yes"), T("No")])
    q6 = st.text_input(T("6. Have you taken any medication or treatment for it? Please specify"))
    q7 = st.radio(T("7. Do you currently have a fever?"), [T("Yes"), T("No")])
    q8 = st.text_input(T("8. Are you experiencing pain anywhere? If yes, where?"))
    q9 = st.radio(T("9. Do you have a cough, cold, or shortness of breath?"), [T("Yes"), T("No")])
    q10 = st.radio(T("10. Have you noticed any change in your appetite or weight?"), [T("Yes"), T("No")])
    q11 = st.text_input(T("11. Do you have any chronic conditions (e.g., diabetes, hypertension, asthma)? Please specify"))
    q12 = st.text_input(T("12. Are you currently taking any medication? Please specify"))
    q13 = st.text_input(T("13. Do you have any known allergies (drug, food, or environmental)? Please Specify"))
    q14 = st.text_input(T("14. Have you been hospitalized or had surgery before?"))
    q15 = st.radio(T("15. Do you smoke or drink alcohol?"), [T("Yes"), T("No")])
    q16 = st.slider(T("16. How many hours of sleep do you get daily?"), 0, 12, 7)
    q17 = st.selectbox(T("17. How often do you exercise or stay physically active?"),
                       [T("Daily"), T("A few times a week"), T("Rarely"), T("Never")])
    q18 = st.radio(T("18. Have you been feeling unusually tired, anxious, or stressed recently?"),
                   [T("Yes"), T("No")])
    q19 = st.radio(T("19. For women: Are you pregnant, breastfeeding, or expecting your period soon?"),
                   [T("Pregnant"), T("Breastfeeding"), T("Expecting period"), T("None of the above")])
    q20 = st.text_area(T("20. Is there anything else you want the doctor to know before your visit?"))

    submitted = st.form_submit_button(T("Book Appointment"))


    if submitted:
        
        # --- VALIDATION CHECK ---
        required_fields = [name, email, q1, q2, q3, q4, q5, q6, q7, q8,
                           q9, q10, q11, q12, q13, q14, q15, q16, q17, q18, q19, q20]

        if any(str(field).strip() == "" for field in required_fields):
            st.error(T("⚠️ Please fill in all fields before submitting the form."))
        else:
            # --- FORM IS COMPLETE ---
            st.success(T(f"Appointment booked successfully for {name} on {date} at {time}."))
            
            data = {
                "Name": [name],
                "Email": [email],
                "Preferred Date": [str(date)],
                "Preferred Time": [str(time)],
                "Problem": [q1],
                "Start_date": [q2],
                "Current_condition_after_start": [q3],
                "Severity": [q4],
                "Occured_Before": [q5],
                "Medication_taken": [q6],
                "Fever": [q7],
                "Pain": [q8],
                "Cough/Cold/Breath_Shortness": [q9],
                "Change_in_appetite/weight": [q10],
                "Chronic_Conditions": [q11],
                "Current_Medication": [q12],
                "Allergies": [q13],
                "Past_Hospitalization/Surgery": [q14],
                "Smoke_or_Alcohol": [q15],
                "Sleep_Hours": [q16],
                "Exercise_Frequency": [q17],
                "Stress/Fatigue": [q18],
                "Women_Status": [q19],
                "Other_Notes": [q20],
                "Submitted_On": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
            }

            df = pd.DataFrame(data)
            filename = f"{name}_{date}_form.csv"
            df.to_csv(filename, index=False)

            send_email(name, filename)
            save_booking_to_db(data)


# --- FOOTER ---
st.markdown(f"""
<footer>
    <hr>
    <p>© 2025 {T("Health Assist")} | {T("MEDGuide❤️")}</p>
</footer>
""", unsafe_allow_html=True)
