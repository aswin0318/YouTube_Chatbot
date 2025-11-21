# YouTube RAG Chatbot (LangChain + FastAPI + Streamlit)

An interactive AI chatbot that analyzes YouTube videos using transcripts and
answers questions using a full RAG (Retrieval-Augmented Generation) pipeline.

### 🔥 Features
- Extracts transcripts using the YouTube Transcript API
- Splits long transcripts into semantic chunks
- Embeds documents using Gemini Embedding Model
- Stores vectors in ChromaDB for retrieval
- Uses Gemini Flash Lite for fast real-time answers
- Full conversational memory
- Clean separation: FastAPI backend + Streamlit UI