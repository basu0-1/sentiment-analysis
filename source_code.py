import streamlit as st
import pickle

model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

st.title("🧠 Personal Diary Sentiment Analyzer")

text = st.text_area("Write your diary entry")

if st.button("Analyze Sentiment"):
    data = vectorizer.transform([text])
    prediction = model.predict(data)

    if prediction[0] == "positive":
        st.success("😊 Positive Mood")
    elif prediction[0] == "negative":
        st.error("😢 Negative Mood")
    else:
        st.info("😐 Neutral Mood")
