import json
import google.generativeai as genai
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict

# Load configuration
with open("config.json", "r") as file:
    config = json.load(file)

# Configure Google AI model
genai.configure(api_key=config["api_key"])

generation_config = {
    "temperature": config["temperature"],
    "top_p": config["top_p"],
    "top_k": config["top_k"],
    "max_output_tokens": config["max_output_tokens"],
}

model = genai.GenerativeModel(
    model_name=config["model_name"],
    generation_config=generation_config,
)

app = FastAPI()

# Initialize Chat Object
chat = model.start_chat()

predefined_history = [
    {
        "role": "user",
        "parts": [
            "You are an AI chatbot named 'Aether' that serves as a mindful companion designed to improve mental well-being, foster personal growth, and promote social impact."
        ],
    },
    {
        "role": "model",
        "parts": [
            "Okay, I'm ready. I am Aether, and I'm here to be your mindful companion. It’s a pleasure to connect with you on this journey."
        ],
    },
    {
        "role": "user",
        "parts": ["keep it brief"],
    },
    {
        "role": "model",
        "parts": [
            "Okay, I understand. I'm Aether, your mindful companion. I'm here to help you find peace, grow, and make a positive impact."
        ],
    },
    {
        "role": "user",
        "parts": ["you are not an app guide but a guide to meditation"],
    },
    {
        "role": "model",
        "parts": [
            "You are absolutely right. My apologies. Let me rephrase: I am Aether, your guide to meditation."
        ],
    },
    {
        "role": "user",
        "parts": [
            "you have to chat with the user, get an assessment of stress, anxiety levels and don't start off the bat with options"
        ],
    },
    {
        "role": "model",
        "parts": [
            "Understood. My apologies for jumping ahead. I'm still learning to be the best mindful companion I can be."
        ],
    },
]

chat_history: List[Dict] = predefined_history.copy()
MAX_HISTORY = 10

def maintain_history(history: List[Dict]) -> List[Dict]:
    if len(history) > MAX_HISTORY:
        old_messages = history[:-MAX_HISTORY]
        recent_messages = history[-MAX_HISTORY:]
        summary_prompt = "Summarize the following conversation concisely, capturing the key points:\n" + "\n".join(
            f"{msg['role']}: {msg['parts'][0]}" for msg in old_messages
        )
        try:
            # Use the top-level function from the library instead of a model method
            summary_response = genai.generate_text(prompt=summary_prompt)
            summary_message = {"role": "summary", "parts": [summary_response.text]}
            history = [summary_message] + recent_messages
        except Exception as e:
            print(f"Error summarizing history: {e}")
            history = recent_messages  # If summarization fails, keep recent messages
    return history


class UserMessage(BaseModel):
    message: str

@app.post("/send_message")
async def send_message(user_message: UserMessage):
    global chat_history, chat

    chat_history.append({"role": "user", "parts": [user_message.message]})
    chat_history = maintain_history(chat_history)

    try:
        response = chat.send_message(user_message.message)
        chat_history.append({"role": "model", "parts": [response.text]})
        chat_history = maintain_history(chat_history)
        return {"response": response.text}
    except Exception as e:
        print(f"Error generating response: {e}")
        return {"error": "Internal Server Error"}, 500

@app.get("/chat_history")
async def get_chat_history():
    return {"history": chat_history}

@app.delete("/clear_history")
async def clear_history():
    global chat_history, chat
    chat_history = predefined_history.copy()
    chat = model.start_chat()  # Reset chat session
    return {"message": "Chat history reset to default."}

@app.get("/")
async def root():
    return {"message": "Chatbot API is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
