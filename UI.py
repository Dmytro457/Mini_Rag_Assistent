import streamlit as st
import requests
import json
import time
  

API_URL = "http://localhost:8000"   
 
st.title("Mini RAG Assistant")
st.markdown("Відповіді на основі PDF-документів")

user_question = st.text_input("Твоє питання:", placeholder="What is Python?")


if st.button("Отримати відповідь") and user_question:
    with st.spinner("Шукаю відповідь..."):
        try:
            response = requests.post(
                f"{API_URL}/generate_answer",
                params = {"user_question": user_question}
            )
            data = response.json()

            st.subheader("Answer:")
            st.write(data['answer'])
 
        except Exception as e:
            st.error(f"Помилка: {e}")
  
  