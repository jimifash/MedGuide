import streamlit as st
from ml_page import page
from train import accuracy
import train

# --- PAGE CONFIG ---
st.set_page_config(page_title="Doctor Access", layout="centered")

# --- AUTHENTICATION CODE ---
ACCESS_CODES = {
    "ADMIN999": "System Admin"
}

# --- SESSION STATE FOR LOGIN PERSISTENCE ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user" not in st.session_state:
    st.session_state.user = None

# --- LOGIN FORM ---
if not st.session_state.authenticated:
    st.title("🔒 Restricted Access")
    st.write("This page is for authorized personnel only.")
    
    access_code = st.text_input("Enter Access Code", type="password")
    if st.button("Login"):
        if access_code in ACCESS_CODES:
            st.session_state.authenticated = True
            st.session_state.user = ACCESS_CODES[access_code]
            st.success(f"Access granted ✅ — Welcome, {st.session_state.user}")
            st.rerun()
        else:
            st.error("❌ Invalid code. Please try again.")
else:
    train()
    page()