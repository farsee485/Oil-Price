from openai import OpenAI
from config import DEEPSEEK_API_KEY

client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com"
)

def ask_deepseek(user_message, history=None):
    """
    Send a message to DeepSeek chat and return the reply.
    history is a list of previous messages (optional).
    """
    if not DEEPSEEK_API_KEY:
        return "DeepSeek API key is not set. Please add it to your .env file."

    messages = []
    if history:
        # Convert Gradio chat history format to OpenAI format
        for msg in history:
            role = "user" if msg["role"] == "user" else "assistant"
            messages.append({"role": role, "content": msg["content"]})
    messages.append({"role": "user", "content": user_message})

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"
