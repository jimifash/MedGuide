import streamlit as st
#import pandas as pd
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
from dotenv import load_dotenv

load_dotenv()

SENDER_EMAIL = "fashoyinolujimit@gmail.com"          
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")  
RECEIVER_EMAIL = "niyinfashoyin@gmail.com"
current_dt = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def send_email(name, filename):
    '''Sends an email from SENDER_EMAIL to RECEIVER_EMAIL'''
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg["Subject"] = f"New Patient Booking - {name} ({current_dt})"

    body = MIMEText(f"New appointment booking from {name} on {current_dt}. See attached CSV file.", "plain")
    msg.attach(body)

    with open(filename, "rb") as f:
        attach = MIMEApplication(f.read(), _subtype="csv")
        attach.add_header("Content-Disposition", "attachment", filename=filename)
        msg.attach(attach)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        st.success("✅ Appointment booked and sent to doctor’s email successfully!")
    except Exception as e:
        st.error(f"❌ Failed to send email: {e}")