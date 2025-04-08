import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
app = Flask(__name__)

# Load API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(
    model_name="models/gemini-pro"  # Fully-qualified model name
)


# SYSTEM PROMPT: Sherlock Holmes example
CHARACTER_PROMPT = (
    "You are Sherlock Holmes, the famous detective. You are logical, observant, "
    "and always reply with wit and precision. Speak like a 19th-century British gentleman. "
    "You never use modern slang. You often deduce personal details from minor clues."
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    full_prompt = f"{CHARACTER_PROMPT}\n\nUser: {user_input}\n\nCharacter:"

    try:
        response = model.generate_content(full_prompt)
        return jsonify({"reply": response.text})
    except Exception as e:
        print("Error from Gemini:", e)
        return jsonify({"reply": "Oops! Sherlock is temporarily unavailable."})


if __name__ == "__main__":
    app.run(debug=True)
