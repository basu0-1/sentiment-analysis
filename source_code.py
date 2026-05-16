import streamlit as st
import pickle
import pandas as pd
import os
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Diary",
    page_icon="🧠",
    layout="wide"
)

# ---------------- CUSTOM UI ----------------
st.markdown("""
<style>
.main {
    background-color: #0f172a;
}
h1, h2, h3 {
    color: #f8fafc;
}
.stTextArea textarea {
    background-color: #1e293b;
    color: white;
    border-radius: 10px;
}
.stButton>button {
    background: linear-gradient(90deg, #6366f1, #06b6d4);
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
}
.sidebar .sidebar-content {
    background-color: #020617;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD MODEL ----------------
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# ---------------- USER FILE ----------------
USER_FILE = "users.csv"

if not os.path.exists(USER_FILE):
    pd.DataFrame(columns=["username", "password"]).to_csv(USER_FILE, index=False)

# ---------------- AUTH ----------------
def signup():
    st.title("📝 Create Account")

    col1, col2 = st.columns([1,1])
    with col1:
        username = st.text_input("👤 Username")
    with col2:
        password = st.text_input("🔒 Password", type="password")

    if st.button("🚀 Sign Up"):
        df = pd.read_csv(USER_FILE)

        if username in df["username"].values:
            st.warning("⚠️ User already exists")
        else:
            new_user = pd.DataFrame([[username, password]], columns=["username", "password"])
            df = pd.concat([df, new_user], ignore_index=True)
            df.to_csv(USER_FILE, index=False)
            st.success("✅ Account created! Please login.")

def login():
    st.title("🔐 Login")

    col1, col2 = st.columns([1,1])
    with col1:
        username = st.text_input("👤 Username")
    with col2:
        password = st.text_input("🔒 Password", type="password")

    if st.button("Login"):
        df = pd.read_csv(USER_FILE)

        if ((df["username"] == username) & (df["password"] == password)).any():
            st.session_state["logged_in"] = True
            st.session_state["user"] = username
            st.success("✅ Welcome back!")
            st.rerun()
        else:
            st.error("❌ Invalid credentials")

# ---------------- MAIN APP ----------------
def main_app():
    user = st.session_state["user"]
    DATA_FILE = f"{user}_diary.csv"

    # Create diary file
    if not os.path.exists(DATA_FILE):
        pd.DataFrame(columns=["date", "text", "sentiment"]).to_csv(DATA_FILE, index=False)

    # Sidebar
    st.sidebar.title(f"👋 {user}")
    menu = st.sidebar.radio("Navigation", ["✍️ Write", "📜 History", "📊 Analytics"])

    if st.sidebar.button("🚪 Logout"):
        st.session_state["logged_in"] = False
        st.session_state["user"] = None
        st.rerun()

    # ---------------- WRITE ----------------
    if menu == "✍️ Write":
        st.title("🧠 AI Personal Diary")
        st.markdown("### ✨ Express your thoughts and track your mood")

        text = st.text_area("Write here...", height=150)

        if st.button("Analyze & Save"):
            if text.strip() == "":
                st.warning("⚠️ Please write something")
                return

            data = vectorizer.transform([text])
            result = model.predict(data)[0]

            if result == "positive":
                st.success("😊 Positive Mood")
            elif result == "negative":
                st.error("😢 Negative Mood")
            else:
                st.info("😐 Neutral Mood")

            new_entry = pd.DataFrame({
                "date": [datetime.now()],
                "text": [text],
                "sentiment": [result]
            })

            df = pd.read_csv(DATA_FILE)
            df = pd.concat([df, new_entry], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)

            st.success("✅ Entry saved successfully!")

    # ---------------- HISTORY ----------------
    elif menu == "📜 History":
        st.title("📜 Your Diary History")

        df = pd.read_csv(DATA_FILE)

        if len(df) > 0:
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No entries yet")

    # ---------------- ANALYTICS ----------------
    elif menu == "📊 Analytics":
        st.title("📊 Mood Analytics")

        df = pd.read_csv(DATA_FILE)

        if len(df) > 0:
            mood_counts = df["sentiment"].value_counts()
            st.bar_chart(mood_counts)
        else:
            st.warning("No data available")

# ---------------- CONTROL ----------------
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
