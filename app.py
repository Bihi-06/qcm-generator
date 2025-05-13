from flask import Flask, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

app = Flask(__name__)

# Get your Gemini API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("❌ GEMINI_API_KEY not found in .env")

# Configure Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

@app.route("/generate_qcm", methods=["POST"])
def generate_qcm():
    data = request.get_json()
    text = data.get("text", "")
    level = data.get("level", 1)
    difficulty = data.get("difficulty", "سهل")

    prompt = f"""
    👇 النص التالي:

    {text}

    ✍️ المستوى: {level} - الصعوبة: {difficulty}
    أنشئ سؤال اختيار من متعدد (QCM) مكوَّن من أربعة اختيارات مع إجابة واحدة صحيحة.

    ✅ اكتب:
    السؤال: ...
    أ. ...
    ب. ...
    ج. ...
    د. ...
    الإجابة: ...
    """

    try:
        response = model.generate_content(prompt)
        return jsonify({"qcm": response.text})  # ✅ Just return the text directly
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)