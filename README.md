
# 🧠 Gemini QCM Generator (Arabic/French)

This is a Flask web application that uses **Google's Gemini API** to automatically generate **QCM (Multiple Choice Questions)** from an input text in **Arabic** or **French**. The generated questions are stored in a **MySQL database** and can be filtered by **difficulty level** and **text ID**.

---

## 🚀 Features

- Supports Arabic 🇸🇦 and French 🇫🇷 texts
- Detects language automatically
- Generates one QCM (question + 4 choices + correct answer)
- Stores QCMs in a MySQL database
- API-ready for integration into web or mobile apps

---

## 🛠️ Technologies Used

- [Flask](https://flask.palletsprojects.com/)
- [Google Generative AI (Gemini)](https://ai.google.dev/)
- [MySQL](https://www.mysql.com/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

---

## 📦 Installation

- Clone the repo:

  ```bash
  git clone https://github.com/your-username/qcm-gemini.git
  cd qcm-gemini
  ```

- Install dependencies:

  ```bash
  pip install -r requirements.txt
  ```

- Set up environment variables by creating a `.env` file:

  ```env
  GEMINI_API_KEY=your_gemini_api_key
  DB_HOST=localhost
  DB_USER=root
  DB_PASSWORD=your_mysql_password
  DB_NAME=agenticia
  ```

- Import the database into MySQL (via phpMyAdmin or CLI):

  ```bash
  mysql -u root -p agenticia < agenticia.sql
  ```

---

## ▶️ Run the App

```bash
python app.py
```

App runs on: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 📮 API Endpoint

### `POST /generate_qcm`

Generate and store a QCM from input text.

- **Request Body Example**

  ```json
  {
    "text": "Votre texte ici en français ou en arabe...",
    "level": 1,
    "difficulty": "facile",
    "idTexte": 2
  }
  ```

- **Response Example**

  ```json
  {
    "message": "✅ QCM generated and stored successfully.",
    "question": "Quelle est la planète la plus proche du Soleil ?",
    "choices": ["Mercure", "Vénus", "Terre", "Mars"],
    "answer": "A"
  }
  ```

---

## 🧪 Testing Examples

- **Arabic Example**

  ```json
  {
    "text": "يتكون النظام الشمسي من الشمس وثمانية كواكب...",
    "level": 1,
    "difficulty": "سهل",
    "idTexte": 1
  }
  ```

- **French Example**

  ```json
  {
    "text": "Le système solaire est composé du Soleil et de huit planètes...",
    "level": 1,
    "difficulty": "facile",
    "idTexte": 2
  }
  ```

---

## 📁 Project Structure

```
.
├── app.py
├── .env
├── requirements.txt
├── agenticia.sql
└── README.md
```

---

## 📌 To-Do

- [ ] Add multi-question generation
- [ ] Build a web frontend (Flask templates or React)
- [ ] Add authentication for API
- [ ] Create endpoints to list/edit/delete QCMs

---

## 📃 License

MIT License — Free to use and modify.

---

## 🙋‍♂️ Author

Built with ❤️ by Ayoub ait said
