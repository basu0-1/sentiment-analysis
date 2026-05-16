import streamlit as st
import pickle
import pandas as pd
import os
from datetime import datetime

# ---------------- CONFIG ----------------
st.set_page_config(page_title="AI Diary App", page_icon="🧠", layout="wide")

# ---------------- LOAD MODEL ----------------
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# ---------------- USER FILE ----------------
USER_FILE = "users.csv"

if not os.path.exists(USER_FILE):
    df = pd.DataFrame(columns=["username", "password"])
    df.to_csv(USER_FILE, index=False)

# ---------------- AUTH FUNCTIONS ----------------
def signup():
    st.subheader("📝 Create Account")

    new_user = st.text_input("Username")
    new_pass = st.text_input("Password", type="password")

    if st.button("Sign Up"):
        df = pd.read_csv(USER_FILE)

        if new_user in df["username"].values:
            st.warning("User already exists")
        else:
            new_data = pd.DataFrame([[new_user, new_pass]], columns=["username", "password"])
            df = pd.concat([df, new_data], ignore_index=True)
            df.to_csv(USER_FILE, index=False)
            st.success("Account created! Please login.")

def login():
    st.subheader("🔐 Login")

    user = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        df = pd.read_csv(USER_FILE)

        if ((df["username"] == user) & (df["password"] == password)).any():
            st.session_state["user"] = user
            st.session_state["logged_in"] = True
            st.success("Login successful")
        else:
            st.error("Invalid credentials")

# ---------------- MAIN APP ----------------
def main_app():
    user = st.session_state["user"]
    DATA_FILE = f"{user}_diary.csv"

    # Create user diary file
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=["date", "text", "sentiment"])
        df.to_csv(DATA_FILE, index=False)

    # Sidebar
    st.sidebar.title(f"👋 Welcome, {user}")
    menu = st.sidebar.radio("📌 Menu", ["Write Entry", "View History", "Analytics"])

    # Logout
    if st.sidebar.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["user"] = None
        st.rerun()

    # -------- WRITE ENTRY --------
    if menu == "Write Entry":
        st.title("🧠 AI Personal Diary")

        text = st.text_area("Write your thoughts...")

        if st.button("Analyze & Save"):
            data = vectorizer.transform([text])
            result = model.predict(data)[0]

            if result == "positive":
                st.success("😊 Positive Mood")
            elif result == "negative":
                st.error("😢 Negative Mood")
            else:
                st.info("😐 Neutral Mood")

            # Save entry
            new_entry = pd.DataFrame({
                "date": [datetime.now()],
                "text": [text],
                "sentiment": [result]
            })

            df = pd.read_csv(DATA_FILE)
            df = pd.concat([df, new_entry], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)

            st.success("Entry saved!")

    # -------- HISTORY --------
    elif menu == "View History":
        st.title("📜 Diary History")

        df = pd.read_csv(DATA_FILE)
        st.dataframe(df)

    # -------- ANALYTICS --------
    elif menu == "Analytics":
        st.title("📊 Mood Analytics")

        df = pd.read_csv(DATA_FILE)

        if len(df) > 0:
            mood_counts = df["sentiment"].value_counts()
            st.bar_chart(mood_counts)
        else:
            st.warning("No data available yet")

# ---------------- APP CONTROL ----------------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

menu = st.sidebar.selectbox("Menu", ["Login", "Signup"])

if st.session_state["logged_in"]:
    main_app()
else:
    if menu == "Login":
        login()
    else:
        signup()
