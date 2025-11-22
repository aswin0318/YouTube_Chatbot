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
        st.sidebar.success("Transcript loaded successfully, you can now ask questions")
        st.session_state.history = []
    else:
        st.warning("Paste the url")

query = st.text_input("Ask Questions")
qa_btn = st.button("Ask AI")

if qa_btn and query and url_inp:
    try:
        response = requests.post(
            "http://127.0.0.1:8000/chat",
            json={
                "url": url_inp,
                "query": query,
                "chat_history": st.session_state.history
            },
            timeout=20
        )

        if response.status_code != 200:
            st.error(f"Server Error ({response.status_code}) - could not process request.")
            st.stop()
        
        data = response.json()

        if "error" in data:
            st.error(f"Transcript Error: {data['error']}")
            st.stop()
        
        if not data.get("chat_history"):
            st.warning("Transcript not available or could not be processed.")
            st.stop()

        st.session_state.history = data["chat_history"]

        for msg in st.session_state.history:
            st.write(f"**{msg['type']}**: {msg['content']}")

    except requests.exceptions.ConnectionError:
        st.error("Backend is not running. Start FastAPI server first.")
        st.stop()
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        st.stop()
