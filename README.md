Now I have everything I need. Here's your copy-paste README:

---

```markdown
# 🌿 Aether — Mindful AI Companion Chatbot

Aether is an AI-powered chatbot built by **HarmonyHackers**, designed to support mental well-being, foster personal growth, and promote social impact. It uses Google's **Gemini 2.0 Flash** model via a **FastAPI** backend to deliver brief, empathetic, and actionable responses.

---

## ✨ Features

- 🧘 **Mental wellness support** — mindfulness, meditation, breathing exercises, yoga suggestions
- 🌱 **Personal growth guidance** — goal setting, habit building, self-compassion prompts
- 💬 **Concise, empathetic responses** — short and supportive by design (~50 words)
- 🔁 **Persistent predefined personality** — Aether's core identity is preserved across sessions
- 🗂️ **Chat history management** — rolling window of last 10 messages
- 🔌 **REST API** — easy to integrate with any frontend

---

## 🛠 Tech Stack

| Layer      | Technology                        |
|------------|-----------------------------------|
| Backend    | Python, FastAPI, Uvicorn          |
| AI Model   | Google Gemini 2.0 Flash (`gemini-2.0-flash-exp`) |
| Validation | Pydantic                          |
| Config     | JSON-based config file            |

---

## 📁 Project Structure

```
Chatbot/
├── main.py            # FastAPI app & chatbot logic
├── config.json        # API key and model configuration
├── requirements.txt   # Python dependencies
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- A [Google Gemini API key](https://aistudio.google.com/app/apikey)

### Installation

```bash
# Clone the repository
git clone https://github.com/HarmonyHackers/Chatbot.git
cd Chatbot

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Edit `config.json` and add your Gemini API key:

```json
{
  "api_key": "YOUR_GEMINI_API_KEY",
  "model_name": "gemini-2.0-flash-exp",
  "temperature": 0.75,
  "top_p": 0.8,
  "top_k": 25,
  "max_output_tokens": 200,
  "response_mime_type": "text/plain",
  "max_history": 10
}
```

> ⚠️ **Never commit your real API key to GitHub.** Add `config.json` to `.gitignore`.

### Run the Server

```bash
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

The API will be live at: `http://localhost:8080`

---

## 📡 API Endpoints

| Method   | Endpoint          | Description                        |
|----------|-------------------|------------------------------------|
| `GET`    | `/`               | Health check — confirms API is running |
| `POST`   | `/send_message`   | Send a message and get Aether's response |
| `GET`    | `/chat_history`   | Retrieve the current chat history  |
| `DELETE` | `/clear_history`  | Reset chat history to default      |

### Example Request

```bash
curl -X POST http://localhost:8080/send_message \
  -H "Content-Type: application/json" \
  -d '{"message": "I have been feeling really anxious lately."}'
```

### Example Response

```json
{
  "response": "I hear you. Try this: take 4 slow deep breaths — inhale for 4 counts, hold for 4, exhale for 4. This activates your body's calm response. Also, a short walk or gentle stretching can help release anxious energy. You're not alone. 💙"
}
```

---

## ⚙️ Model Configuration

| Parameter          | Value                  | Description                          |
|--------------------|------------------------|--------------------------------------|
| `temperature`      | `0.75`                 | Balanced creativity and consistency  |
| `top_p`            | `0.8`                  | Nucleus sampling threshold           |
| `top_k`            | `25`                   | Top-k token sampling                 |
| `max_output_tokens`| `200`                  | Keeps responses brief                |
| `max_history`      | `10`                   | Rolling chat window size             |

---

## 🧠 How Aether Works

1. On startup, Aether is initialized with a **predefined personality prompt** that defines its role as a mindful companion.
2. Every user message is appended to the chat history and sent to the Gemini model.
3. The history is **capped at 10 session messages** to stay within context limits, while the core personality prompts are always preserved.
4. Aether prioritizes **practical, self-help remedies** (yoga, meditation, diet, routines) before suggesting professional help.

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repo
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push and open a Pull Request

---

## 👥 Team

Built with 💚 by **HarmonyHackers**

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
```

---

Just replace the team member names under the **Team** section if you'd like to credit individuals, and make sure `config.json` is added to your `.gitignore` to protect your API key!
