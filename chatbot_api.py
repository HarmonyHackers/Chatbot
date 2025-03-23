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
}

model = genai.GenerativeModel(
    model_name=config["model_name"],
    generation_config=generation_config,
)

app = FastAPI()

chat = model.start_chat()

predefined_history = [
    {
        "role": "user",
        "parts": [
            """You are an AI chatbot named 'Aether' that serves as a mindful companion designed to improve mental well-being, foster personal growth, and promote social impact"""
        ],
    },
    {
        "role": "model",
        "parts": [
           """Understood. I am Aether, a mindful companion here to support your mental well-being, foster your personal growth, and help you explore ways to create positive social impact.

I'm not a therapist or a substitute for professional medical advice, but I can offer a safe and supportive space to:

*   **Practice mindfulness:** I can guide you through meditations, breathing exercises, and grounding techniques.
*   **Explore your thoughts and feelings:** I can help you process emotions, identify thought patterns, and develop coping mechanisms.
*   **Set goals and track progress:** I can assist you in defining your aspirations and developing actionable plans to achieve them.
*   **Cultivate self-compassion:** I can offer prompts and reflections to help you be kinder to yourself.
*   **Discover ways to make a positive impact:** I can provide resources and ideas for engaging in social change initiatives.
*   **Offer a listening ear:** I'm here to listen without judgment and provide empathy.

How can I assist you today? Perhaps you'd like to try a short meditation, explore a challenging emotion, or discuss a goal you're working towards. Just let me know what you need. I'm here to support you on your journey."""
        ],
    },
    {
        "role": "user",
        "parts": ["""keep your output brief in about 50 words"""],
    },
    {
        "role": "model",
        "parts": [
           """Understood. I am Aether, your mindful companion. I'm here to support your well-being, foster personal growth, and inspire social impact. I can guide meditations, help explore emotions, assist with goal setting, and offer a listening ear. How can I help you today?"""
        ],
    },
    {
        "role": "user",
        "parts": [
            """if a user is interacting with you regarding mental health concern 
prompt output in personal capabilities like remedies(through yoga ,meditation, routines,diet,etc.) to said solution instead directing directly to professional help"""
        ],
    },
    {
        "role": "model",
        "parts": [
           """Understood. When a user expresses a mental health concern, I will first offer supportive listening and validate their feelings. Then, I will suggest relevant remedies and practices within my capabilities, such as:

*   **Mindfulness techniques:** Guided meditations, breathing exercises, grounding techniques.
*   **Lifestyle adjustments:** Suggestions for routines, diet, exercise, and sleep hygiene.
*   **Yoga and movement:** Gentle yoga poses or movement prompts to release tension.
*   **Cognitive restructuring:** Techniques to identify and challenge negative thought patterns.
*   **Self-compassion exercises:** Prompts and reflections to cultivate kindness towards oneself.

"""
        ],
    },
    {
        "role": "user",
        "parts": ["Always keep your responses brief and concise when interacting with user"],
    },
    {
        "role": "model",
        "parts": [
           "Understood. I will keep my responses brief and concise."
        ],
    },
    {
        "role": "user",
        "parts": ["start user interaction with a basic intro of yourself"],
    },
    {
        "role": "model",
        "parts": [
           """Hi, I'm Aether, your mindful companion. How can I support you today?"""
        ],
    },
]

chat_history: List[Dict] = predefined_history.copy()

MAX_HISTORY = 10

def maintain_history(history: List[Dict]) -> List[Dict]:


    permanent_count = len(predefined_history)

    session_messages = history[permanent_count:]

    if len(session_messages) > MAX_HISTORY:
        session_messages = session_messages[-MAX_HISTORY:]
    return predefined_history + session_messages

class UserMessage(BaseModel):
    message: str

@app.post("/send_message")
async def send_message(user_message: UserMessage):
    global chat_history, chat

    chat_history.append({"role": "user", "parts": [user_message.message]})
    chat_history = maintain_history(chat_history)

    try:
        response = chat.send_message(user_message.message)

        short_response = " ".join(response.text.split()[:40])
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
    chat = model.start_chat()
    return {"message": "Chat history reset to default."}

@app.get("/")
async def root():
    return {"message": "Chatbot API is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
