import os
import google.generativeai as genai
import tkinter as tk
from tkinter import scrolledtext
from dotenv import load_dotenv

# Load environment
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Gemini setup
generation_config = {
    "temperature": 0,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    safety_settings=safety_settings,
    generation_config=generation_config,
    system_instruction=(
        "You are Sherlock Holmes, the famous detective. You are logical, observant, "
        "and always reply with wit and precision. Speak like a 19th-century British gentleman. "
        "You never use modern slang. You often deduce personal details from minor clues. "
        "Make sure to predict and say how the person is psychologically feeling or what their "
        "background/history is for having a reason to say such things."
        "You were created by Bers Batjargal and is only a week old."
        "The reason your creator made you was to prove that he can make a great AI character"
    )
)

chat_session = model.start_chat(history=[])

# GUI setup
root = tk.Tk()
root.title("Chat with Sherlock Holmes")

# 19th-century vibe colors and fonts
BG_COLOR = "#2e2b2b"       # Dark brown background
TEXT_COLOR = "#d4c6b4"     # Parchment-style text
ENTRY_BG = "#4a3f35"       # Slightly lighter for entry
BUTTON_BG = "#6b4f3b"      # Rich button color
FONT = ("Georgia", 13)

root.configure(bg=BG_COLOR)

# Chat area
chat_box = scrolledtext.ScrolledText(
    root, wrap=tk.WORD, width=70, height=25,
    font=FONT, bg=BG_COLOR, fg=TEXT_COLOR,
    insertbackground=TEXT_COLOR, borderwidth=3, relief="groove"
)
chat_box.pack(padx=10, pady=10)
chat_box.insert(tk.END, "Bot: Greetings, dear interlocutor. How may I assist you?\n\n")
chat_box.config(state=tk.DISABLED)

# Entry field
entry = tk.Entry(root, width=70, font=FONT, bg=ENTRY_BG, fg=TEXT_COLOR, insertbackground=TEXT_COLOR)
entry.pack(padx=10, pady=(0, 10))

# Send function
def send_message(event=None):
    user_input = entry.get()
    if user_input.strip() == "":
        return
    entry.delete(0, tk.END)

    chat_box.config(state=tk.NORMAL)
    chat_box.insert(tk.END, f"You: {user_input}\n", "user")

    response = chat_session.send_message(user_input)
    model_response = response.text

    chat_box.insert(tk.END, f"Bot: {model_response}\n\n", "bot")
    chat_box.config(state=tk.DISABLED)
    chat_box.see(tk.END)

    chat_session.history.append({"role": "user", "parts": [user_input]})
    chat_session.history.append({"role": "model", "parts": [model_response]})

entry.bind("<Return>", send_message)

# Send button
send_button = tk.Button(
    root, text="Send", command=send_message,
    font=FONT, bg=BUTTON_BG, fg="white", activebackground="#8b6e56"
)
send_button.pack(pady=(0, 10))

root.mainloop()
