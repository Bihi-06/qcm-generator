from flask import Flask, request, jsonify
import google.generativeai as genai
import mysql.connector
import os
from dotenv import load_dotenv
import re

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("❌ GEMINI_API_KEY not found in .env")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

# Connect to MySQL database
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

# Detect whether the input text is Arabic or French
def detect_language(text):
    if re.search(r'[\u0600-\u06FF]', text):
        return "ar"
    return "fr"

# Parse the QCM result returned by Gemini
def parse_qcm_response(text):
    print("🧠 Gemini raw output:\n", text)

    # Remove markdown bold formatting
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)

    # Arabic QCM format
    question_ar = re.search(r"السؤال:\s*(.+)", text)
    options_ar = re.findall(r"(?:أ|ب|ج|د)\.\s*(.+)", text)
    answer_ar = re.search(r"الإجابة:\s*([أبجد])", text)

    # French QCM format
    question_fr = re.search(r"Question:\s*(.+)", text, re.IGNORECASE)
    options_fr = re.findall(r"(?:A|B|C|D)\.\s*(.+)", text)
    answer_fr = re.search(r"Réponse:\s*([A-D])", text, re.IGNORECASE)

    if question_ar and len(options_ar) >= 4 and answer_ar:
        return question_ar.group(1).strip(), options_ar[:4], answer_ar.group(1).strip()

    if question_fr and len(options_fr) >= 4 and answer_fr:
        return question_fr.group(1).strip(), options_fr[:4], answer_fr.group(1).strip()

    raise ValueError("❌ Failed to parse QCM structure from Gemini response.")

@app.route("/generate_qcm", methods=["POST"])
def generate_qcm():
    data = request.get_json()
    text = data.get("text", "")
    level = data.get("level", 1)
    difficulty = data.get("difficulty", "سهل")
    idTexte = data.get("idTexte", None)

    if not text:
        return jsonify({"error": "No input text provided."}), 400

    lang = detect_language(text)

    # Generate the prompt based on the detected language
    if lang == "ar":
        prompt = f"""
        📘 النص التالي:

        {text}

        ✍️ المستوى: {level} - الصعوبة: {difficulty}

        🎯 أنشئ سؤال اختيار من متعدد (QCM) باللغة العربية مكوَّن من أربعة اختيارات مع إجابة واحدة صحيحة.

        ✅ استخدم هذا التنسيق فقط:

        السؤال: ...
        أ. ...
        ب. ...
        ج. ...
        د. ...
        الإجابة: ...
        """
    else:
        prompt = f"""
        📘 Texte suivant :

        {text}

        ✍️ Niveau : {level} - Difficulté : {difficulty}

        🎯 Générez une question à choix multiples (QCM) en français avec quatre options et une seule bonne réponse.

        ✅ Utilisez exactement ce format :

        Question: ...
        A. ...
        B. ...
        C. ...
        D. ...
        Réponse: ...
        """

    try:
        response = model.generate_content(prompt)
        qcm_text = response.text

        # Parse QCM
        question, choices, answer = parse_qcm_response(qcm_text)

        # Format combined choices
        if answer in ['أ', 'ب', 'ج', 'د']:
            choix_combined = f"أ. {choices[0]}\nب. {choices[1]}\nج. {choices[2]}\nد. {choices[3]}"
        else:
            choix_combined = f"A. {choices[0]}\nB. {choices[1]}\nC. {choices[2]}\nD. {choices[3]}"

        # Insert into DB
        conn = get_db_connection()
        cursor = conn.cursor()

        insert_query = """
            INSERT INTO qcm (idTexte, question, choix, reponse)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_query, (idTexte, question, choix_combined, answer))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({
            "message": "✅ QCM generated and stored successfully.",
            "question": question,
            "choices": choices,
            "answer": answer
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)