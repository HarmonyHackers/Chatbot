import json
import google.generativeai as genai
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict

with open("config.json", "r") as file:
    config = json.load(file)

genai.configure(api_key=config["api_key"])

generation_config = {
    "temperature": config["temperature"],
    "top_p": config["top_p"],
    "top_k": config["top_k"],
    "max_output_tokens": config["max_output_tokens"],
    "response_mime_type": config["response_mime_type"],
}

model = genai.GenerativeModel(
    model_name=config["model_name"],
    generation_config=generation_config,
)

app = FastAPI()

chat_history = []

class UserMessage(BaseModel):
    message: str

@app.post("/send_message")
async def send_message(user_message: UserMessage):

    global chat_history
    chat_history.append({"role": "user", "parts": [user_message.message]})

    response = model.start_chat(history=chat_history).send_message(user_message.message)

    chat_history.append({"role": "model", "parts": [response.text]})

    return {"response": response.text}

@app.get("/chat_history")
async def get_chat_history():
    return {"history": chat_history}

@app.delete("/clear_history")
async def clear_chat_history():
    global chat_history
    chat_history = []
    return {"message": "Chat history cleared"}
