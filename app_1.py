"""
==========================================================
Smart Health Risk Predictor
==========================================================

Developed by: Aadhith B

Description:
A Streamlit-based Health Risk Prediction System that
calculates BMI, predicts health risk using multiple
health parameters, stores user records in SQL Server,
and visualizes health trends with Plotly dashboards.

Technologies:
- Python
- Streamlit
- SQL Server
- Plotly
- Pandas
- bcrypt
==========================================================
"""
import streamlit as st
import pyodbc
import bcrypt
import smtplib
import os
import random
import string
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from email.message import EmailMessage
from datetime import datetime

# ---------------- DATABASE ----------------
def get_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=<YOUR_SQL_SERVER_INSTANCE>;" # Replace with your SQL Server instance name
        "DATABASE=HealthAppDB;"
        "Trusted_Connection=yes;"
    )

# ---------------- EMAIL ----------------
def send_email(to_email, subject, body):
    sender_email = os.getenv("EMAIL")# Email credentials are loaded from environment variables.
    app_password = os.getenv("APP_PASSWORD")# Replace with your own EMAIL and APP_PASSWORD before running.

    msg = EmailMessage()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, app_password)
        server.send_message(msg)

# ---------------- TEMP PASSWORD ----------------
def generate_temp_password():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

# ---------------- RISK CALCULATION ----------------
def calculate_risk(bmi, diabetes, sugar, bp, sys, dia, stress, alcohol, smoking):
    risk = 0

    if bmi < 18.5:
        risk += 10
    elif bmi <= 24.9:
        risk += 5
    elif bmi <= 29.9:
        risk += 20
    elif bmi <= 34.9:
        risk += 35
    else:
        risk += 50

    if diabetes:
        if sugar < 140:
            risk += 10
        elif sugar <= 199:
            risk += 20
        else:
            risk += 30

    if bp:
        if sys >= 140 or dia >= 90:
            risk += 25
        elif sys >= 120 or dia >= 80:
            risk += 15

    risk += stress * 2
    risk += alcohol * 2
    risk += smoking * 3

    return min(risk, 100)

# ---------------- SESSION ----------------
if "page" not in st.session_state:
    st.session_state.page = "login"

st.set_page_config(page_title="Smart Health Risk Predictor")
st.title("Smart Health Risk Predictor")

# =====================================================
# LOGIN PAGE
# =====================================================
if st.session_state.page == "login":

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM Users WHERE username=?", username)
        row = cursor.fetchone()

        if row and bcrypt.checkpw(password.encode(), row[0].encode()):
            st.session_state.username = username
            st.session_state.page = "dashboard"
            st.rerun()
        else:
            st.error("Invalid Username or Password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Register"):
            st.session_state.page = "register"
            st.rerun()

    with col2:
        if st.button("Forgot Password"):
            st.session_state.reset_user = username
            st.session_state.page = "forgot"
            st.rerun()

# =====================================================
# REGISTER PAGE
# =====================================================
elif st.session_state.page == "register":

    name = st.text_input("Full Name")
    username = st.text_input("Username")
    dob = st.date_input("DOB",
                        min_value=datetime(1940,1,1),
                        max_value=datetime(2008,12,31))
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Create Account"):

        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Users WHERE username=?", username)
        if cursor.fetchone():
            st.error("Username already exists")
        else:
            cursor.execute("""
                INSERT INTO Users (name, username, dob, email, password)
                VALUES (?, ?, ?, ?, ?)
            """, name, username, dob, email, hashed.decode())
            conn.commit()
            st.success("Account Created")
            st.session_state.page = "login"
            st.rerun()

    if st.button("Back"):
        st.session_state.page = "login"
        st.rerun()
# =====================================================
# FORGOT PASSWORD PAGE
# =====================================================
elif st.session_state.page == "forgot":

    st.subheader("Forgot Password")

    username = st.text_input("Enter Username")

    if st.button("Send Temporary Password"):

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT email FROM Users WHERE username=?", username)
        row = cursor.fetchone()

        if row:
            email = row[0]
            temp_pass = generate_temp_password()
            hashed_temp = bcrypt.hashpw(temp_pass.encode(), bcrypt.gensalt())

            cursor.execute(
                "UPDATE Users SET temp_password=? WHERE username=?",
                hashed_temp.decode(),
                username
            )
            conn.commit()

            send_email(email, "Temporary Password",
                       f"Your temporary password is: {temp_pass}")

            st.session_state.reset_user = username
            st.success("Temporary password sent to your email.")
            st.session_state.page = "verify"
            st.rerun()
        else:
            st.error("Username not found")

    if st.button("Back"):
        st.session_state.page = "login"
        st.rerun()


# =====================================================
# VERIFY TEMP PASSWORD PAGE
# =====================================================
elif st.session_state.page == "verify":

    st.subheader("Verify Temporary Password")

    temp_input = st.text_input("Enter Temporary Password", type="password")

    if st.button("Verify"):

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT temp_password FROM Users WHERE username=?",
            st.session_state.reset_user
        )
        row = cursor.fetchone()

        if row and bcrypt.checkpw(temp_input.encode(), row[0].encode()):
            st.session_state.page = "reset"
            st.rerun()
        else:
            st.error("Invalid Temporary Password")


# =====================================================
# RESET PASSWORD PAGE
# =====================================================
elif st.session_state.page == "reset":

    st.subheader("Reset Password")

    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Update Password"):

        if new_password != confirm_password:
            st.error("Passwords do not match")
        else:
            hashed = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE Users
                SET password=?, temp_password=NULL
                WHERE username=?
            """, hashed.decode(), st.session_state.reset_user)

            conn.commit()
            st.success("Password Updated Successfully")
            st.session_state.page = "login"
            st.rerun()
# =====================================================
# DASHBOARD
# =====================================================
elif st.session_state.page == "dashboard":

    st.subheader("Health Risk Predictor")

    conn = get_connection()
    cursor = conn.cursor()

    location = st.text_input("Your Location (City)")

    height = st.number_input("Height (cm)", 50.0, 200.0)
    weight = st.number_input("Weight (kg)", 20.0, 300.0)

    bmi = weight / ((height/100)**2)
    st.metric("BMI", round(bmi,2))

    diabetes = st.radio("Diabetes?", ["No","Yes"]) == "Yes"
    sugar = st.number_input("Blood Sugar", 70.0, 400.0) if diabetes else 0

    bp = st.radio("High BP?", ["No","Yes"]) == "Yes"
    sys = st.number_input("Systolic", 80.0, 250.0) if bp else 0
    dia = st.number_input("Diastolic", 50.0, 150.0) if bp else 0

    stress = st.slider("Stress Level", 0, 10)
    alcohol = st.slider("Alcohol Level", 0, 10)
    smoking = st.slider("Smoking Level", 0, 10)

    if st.button("Save Record"):

        risk = calculate_risk(
            bmi, diabetes, sugar,
            bp, sys, dia,
            stress, alcohol, smoking
        )

        cursor.execute("""
            INSERT INTO HealthDetails
            (username, height, weight, bmi,
             diabetes, diabetes_level,
             bp, systolic, diastolic,
             stress_level, alcohol_level,
             smoking_level, risk_percentage,
             created_at, location)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        st.session_state.username,
        height, weight, bmi,
        1 if diabetes else 0,
        sugar,
        1 if bp else 0,
        sys,
        dia,
        stress,
        alcohol,
        smoking,
        risk,
        datetime.now(),
        location
        )

        conn.commit()

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=risk,
            title={'text': "Health Risk %"},
            gauge={
                'axis': {'range': [0,100]},
                'bar': {'color': "#00BFFF"},
                'steps': [{'range': [0,100], 'color': "#1a1a1a"}]
            }
        ))

        fig.update_layout(template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

        if risk > 60:
            st.error("HIGH RISK DETECTED")

            st.subheader("Recommended Specialists Near You")
            st.write(f"City: {location}")
            st.write("• Cardiologist")
            st.write("• Diabetologist")
            st.write("• Internal Medicine Specialist")

            st.markdown("### Book Online Consultation")
            st.markdown("[Apollo 24/7](https://www.apollo247.com/)")
            st.markdown("[Practo](https://www.practo.com/)")
            st.markdown("[Tata 1mg](https://www.1mg.com/)")

        elif risk > 30:
            st.warning("Moderate Risk - Consider consulting a specialist.")
            st.markdown("[Optional Consultation - Practo](https://www.practo.com/)")

        else:
            st.success("Low Risk - Maintain healthy lifestyle.")

    # -------- TREND --------
    st.subheader("Risk Trend")

    cursor.execute("""
        SELECT risk_percentage, created_at
        FROM HealthDetails
        WHERE username=?
        ORDER BY created_at ASC
    """, st.session_state.username)

    records = cursor.fetchall()

    if records:
        df = pd.DataFrame.from_records(records)
        df.columns = ["risk", "date"]
        fig2 = px.line(df, x="date", y="risk",
                       markers=True,
                       title="Health Risk Trend")
        fig2.update_layout(template="plotly_dark")
        st.plotly_chart(fig2, use_container_width=True)

    if st.button("Logout"):
        st.session_state.page = "login"
        st.rerun()