import os
import json
from groq import Groq

client = Groq(
    # This is the default and can be omitted
    api_key=os.environ.get("GROQ_API_KEY"),
)

SESSIONS_FOLDER = "chat_sessions"
os.makedirs(SESSIONS_FOLDER, exist_ok=True)

def save_session(history, session_name):
    session_path = os.path.join(SESSIONS_FOLDER, f"{session_name}.json")
    with open(session_path, 'w') as f:
        json.dump(history, f)
    print(f"Session saved to {session_path}")

def load_session(session_name):
    session_path = os.path.join(SESSIONS_FOLDER, f"{session_name}.json")
    if os.path.exists(session_path):
        with open(session_path, 'r') as f:
            history = json.load(f)
        print(f"Session loaded from {session_path}")
        return history
    else:
        print(f"No session found with the name {session_name}")
        return None

def generate_text(prompt, history=None):
    if history is None:
        history = [
            {"role": "system", "content": "You are a helpful assistant. Provide concise and accurate information."}
        ]
    
    history.append({"role": "user", "content": prompt})
    
    chat_completion = client.chat.completions.create(
        messages=history,
        model="llama3-8b-8192",
    )
    
    response = chat_completion.choices[0].message.content
    history.append({"role": "assistant", "content": response})
    
    return response, history

    save_session(chat_history, session_name)
