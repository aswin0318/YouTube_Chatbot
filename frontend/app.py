import streamlit as st
import requests

st.set_page_config(page_title="YouTube QA ChatBot",layout= "wide",page_icon='🤖')

if 'history' not in st.session_state:
    st.session_state.history = []

st.title("YouTube QA ChatBot")

url_inp = st.sidebar.text_input("Paste YouTube video url")
url_btn =st.sidebar.button("Submit")

if url_btn:
    if url_inp:
        st.success("Transcript loaded successfully, you can now ask questions")
        st.session_state.history = []
    else:
        st.warning("Paste the url")

query = st.text_input("Ask Questions")
qa_btn = st.button("Ask AI")

if qa_btn and query and url_inp:
    response = requests.post("http://127.0.0.1:8000/chat",
        json={
            "url" :  url_inp,
            "query" : query,
            "chat_history" : st.session_state.history
        })
    data = response.json()
    st.session_state.history = data['chat_history']

    for msg in st.session_state.history:
        st.write(f"**{msg['type']}**: {msg['content']}")