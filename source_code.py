import streamlit as st
import pickle

model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

st.title("🧠 Advanced Sentiment Analyzer")

text = st.text_area("Write your thoughts...")

if st.button("Analyze"):
    data = vectorizer.transform([text])
    result = model.predict(data)[0]

    if result == "positive":
        st.success("😊 Positive Mood")
    elif result == "negative":
        st.error("😢 Negative Mood")
    else:
        st.info("😐 Neutral Mood")