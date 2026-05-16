import streamlit as st
import pickle
import pandas as pd
from datetime import datetime
import os

# Load model
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

st.set_page_config(page_title="AI Diary", page_icon="🧠", layout="wide")

# ---------------- FILE STORAGE ----------------
DATA_FILE = "diary_data.csv"

if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["date", "text", "sentiment"])
    df.to_csv(DATA_FILE, index=False)

# ---------------- SIDEBAR ----------------
menu = st.sidebar.radio("📌 Menu", ["Write Entry", "View History", "Analytics"])

# ---------------- WRITE ENTRY ----------------
if menu == "Write Entry":
    st.title("🧠 AI Personal Diary")

    text = st.text_area("Write your thoughts...")

    if st.button("Analyze & Save"):
        data = vectorizer.transform([text])
        result = model.predict(data)[0]

        if result == "positive":
            mood = "😊 Positive"
            st.success(mood)
        elif result == "negative":
            mood = "😢 Negative"
            st.error(mood)
        else:
            mood = "😐 Neutral"
            st.info(mood)

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

# ---------------- HISTORY ----------------
elif menu == "View History":
    st.title("📜 Diary History")

    df = pd.read_csv(DATA_FILE)
    st.dataframe(df)

# ---------------- ANALYTICS ----------------
elif menu == "Analytics":
    st.title("📊 Mood Analytics")

    df = pd.read_csv(DATA_FILE)

    if len(df) > 0:
        mood_counts = df["sentiment"].value_counts()
        st.bar_chart(mood_counts)
    else:
        st.warning("No data available yet")
