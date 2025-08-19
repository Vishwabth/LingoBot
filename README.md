
# LingoBot – Conversational Chatbot for Communication Skills  

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)  
[![Django](https://img.shields.io/badge/Django-4.x-green.svg)](https://www.djangoproject.com/)  
[![Transformers](https://img.shields.io/badge/Transformers-HuggingFace-yellow.svg)](https://huggingface.co/)  
[![License: MIT](https://img.shields.io/badge/License-MIT-orange.svg)](LICENSE)  

LingoBot is an **AI-powered chatbot** designed to help users **improve communication, grammar, and sentiment awareness** through interactive conversations. It integrates **NLP pipelines** (grammar correction, sentiment, emotion detection, spell check) with a **lightweight Django + Bootstrap web interface**.  

---

## 🚀 Features  
- **Grammar Correction** – powered by Hugging Face `flan-t5`.  
- **Sentiment Analysis** – detects tone of user messages.  
- **Emotion Detection** – classifies emotional state.  
- **Spell Checking** – word-level correction with `pyspellchecker`.  
- **Text Preprocessing Rules** – rule-based cleaning + spaCy.  
- **Interactive Chat UI** – responsive, simple, user-friendly.  

---

## 📂 Project Structure  
```bash
lingobot_project/
│── db.sqlite3
│── manage.py
│── README.md
│── requirements.txt
│
├── chatbot/
│ ├── admin.py
│ ├── apps.py
│ ├── constants.py
│ ├── models.py
│ ├── nlp.py
│ ├── text_rules.py
│ ├── urls.py
│ ├── utils.py
│ ├── utils_diff.py
│ ├── views.py
│ ├── init.py
│ │
│ ├── static/
│ │ └── chatbot/
│ │ ├── chat.css
│ │ ├── chat.js
│ │
│ ├── templates/
│ │ └── chatbot/
│ │ ├── chat.html
│ │ ├── home.html
│
├── lingobot/
│ ├── asgi.py
│ ├── settings.py
│ ├── urls.py
│ ├── wsgi.py
│ ├── init.py
```

---

## ⚙️ Installation & Setup  

### 1. Clone the Repository  
```bash
git clone https://github.com/<your-username>/LingoBot.git
cd LingoBot/lingobot_project
```
## 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate       # Windows
```
## 4. Apply Migrations
```bash
python manage.py migrate
```
## 5. Run the Development Server
``` bash
python manage.py runserver

```
Now visit 👉 http://127.0.0.1:8000/home/

### 🧠 Tech Stack
- Backend: Django, Python
- Frontend: Bootstrap 5, JavaScript
- NLP Models: Hugging Face Transformers (flan-t5, DistilRoBERTa)
- Libraries: spaCy, PySpellChecker, NumPy

### 📊 Example NLP Pipeline
User Input:
```bash
I has went to the park yesturday.
```
Bot Response:
✏️ Grammar Correction → I went to the park yesterday.
📝 Spell Check → yesturday → yesterday
🎭 Sentiment → Neutral
💡 Emotion → Calm



