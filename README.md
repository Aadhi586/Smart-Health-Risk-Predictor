# 🩺 Smart Health Risk Predictor

A Smart Health Risk Prediction System developed using **Python**, **Streamlit**, **SQL Server**, **Plotly**, and **bcrypt authentication**. The application predicts health risks based on BMI, diabetes, blood pressure, stress, alcohol consumption, and smoking habits while providing interactive dashboards and specialist recommendations.

---

## 🚀 Features

- 🔐 Secure User Registration & Login
- 🔑 Password Encryption using bcrypt
- 📧 Forgot Password with Email Verification
- ❤️ Automatic BMI Calculation
- 📊 Health Risk Prediction
- 📈 Interactive Health Risk Dashboard
- 📉 Risk Trend Visualization
- 💾 SQL Server Database Integration
- 🩺 Specialist Recommendations based on Risk Level
- 🌐 Online Consultation Links
- 📍 Location-based Health Records

---

## 🛠️ Technologies Used

- Python
- Streamlit
- SQL Server
- PyODBC
- Plotly
- Pandas
- bcrypt
- SMTP (Email)
- HTML/CSS (Streamlit UI)

---

## 📂 Project Structure

```
Smart-Health-Risk-Predictor/
│
├── database/
│   └── schema.sql
│
├── screenshots/
│   ├── Login Page.png
│   ├── Registration Page.png
│   ├── Health Risk.png
│   ├── Risk Trend.png
│   ├── Details Uploading - 1.png
│   └── Details Uploading - 2.png
│
├── app_1.py
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

---

## 📸 Application Screenshots

### Login Page

![Login](screenshots/Login%20Page.png)

---

### Registration Page

![Registration](screenshots/Registration%20Page.png)

---

### Health Risk Dashboard

![Health Risk](screenshots/Health%20Risk.png)

---

### Risk Trend

![Risk Trend](screenshots/Risk%20Trend.png)

---

## ⚙️ Installation

### Clone the Repository

```bash
git clone https://github.com/Aadhi586/Smart-Health-Risk-Predictor.git
```

### Navigate to the Project

```bash
cd Smart-Health-Risk-Predictor
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure SQL Server

1. Create the database using `database/schema.sql`.
2. Update the SQL Server connection details in the application.
3. Configure your email credentials if using the password recovery feature.

### Run the Application

```bash
streamlit run app_1.py
```

---

## 🗄️ Database

The project uses Microsoft SQL Server.

Main Tables:

- Users
- HealthDetails
- HealthData

The database schema is available in:

```
database/schema.sql
```

---

## 📊 Health Parameters Considered

- Height
- Weight
- BMI
- Diabetes
- Blood Sugar Level
- Blood Pressure
- Stress Level
- Alcohol Consumption
- Smoking Habits

---

## 🎯 Future Enhancements

- 🤖 AI-Based Disease Prediction
- 📱 Mobile Application
- ☁️ Cloud Database Integration
- 📄 PDF Health Report Generation
- 🧠 Machine Learning Risk Prediction
- 👨‍⚕️ Hospital API Integration
- 📅 Appointment Booking System

---

## 👨‍💻 Author

**Aadhith B**

B.Tech Artificial Intelligence & Data Science

---

## 📜 License

This project is licensed under the MIT License.

---

⭐ If you found this project useful, consider giving it a **Star** on GitHub!
