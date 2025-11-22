#API Endpoints for the application
from fastapi import FastAPI
from backend.yt_bot_logic import process_request
from pydantic import BaseModel

app = FastAPI()

class Chat_Request(BaseModel):
    url: str
    query: str
    chat_history: list = []

class Chat_Response(BaseModel):
    answer: str
    chat_history: list

@app.post('/chat',response_model=Chat_Response)
def chat_api(response : Chat_Request):
    answer,updated_history = process_request(
        url = response.url,
        query = response.query,
        chat_history = response.chat_history
    )
    return Chat_Response(answer=answer,chat_history=updated_history)

@app.get('/')
def home():
    return {"message"  : "API is running....."}
